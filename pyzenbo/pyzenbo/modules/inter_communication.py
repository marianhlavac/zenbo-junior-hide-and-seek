import json
import os
import queue
import threading
import time

import pyzenbo.modules.error_code as error_code
import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.socket_state_machine import SOCKET_STATE
from pyzenbo.modules.socket_state_machine import SOCKET_TYPE
from pyzenbo.modules.socket_state_machine import SocketStateMachine

DESTINATION = {'commander': 1, 'coordinator': 2, 'vision': 3, 'system': 4, 'sensor': 5}
STATE = {0: 'INITIAL', 1: 'PENDING', 2: 'REJECTED',
         3: 'ACTIVE', 4: 'FAILED', 5: 'SUCCEED', 6: 'PREEMPTED', }
_serial = 0


def init_common(cmd, _hash=0, priority=0, pid=os.getpid(), user=""):
    return Common(**{"hash": _hash, "cmd": cmd, "priority": priority,
                     "pid": pid, "user": user})


def get_packet(des, cmd, data):
    common = init_common(cmd)
    return json.dumps({'TYPE': des, 'COMMON': common.get_json(),
                       'DATA': json.dumps(data)}), common.get_serial()


class Common:
    """docstring for Common()"""

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.kwargs.setdefault("hash", 0)
        self.kwargs.setdefault("pid", os.getpid())
        self.kwargs.setdefault("user", "")
        self.kwargs.setdefault("priority", 0)
        self.kwargs.setdefault("version", 0)
        self.kwargs.setdefault("ignoreIdle", False)
        self.kwargs.setdefault("ignorePreempted", False)

    @staticmethod
    def _get_serial():
        global _serial
        _serial += 1
        return _serial

    def get_serial(self):
        return self.kwargs['serial']

    def get_json(self):
        self.kwargs["serial"] = self._get_serial()
        return json.dumps(self.kwargs)


class InterComm:
    """docstring for _InterComm"""

    def __init__(self, destination, on_state_change_callback,
                 on_result_callback, timeout=2):
        self._on_state_change_callback_lock = threading.RLock()
        self._on_result_callback_lock = threading.RLock()
        self._listen_callback_lock = threading.RLock()
        self._vision_callback_lock = threading.RLock()
        self.on_state_change_callback = on_state_change_callback
        self.on_result_callback = on_result_callback
        self.listen_callback = None
        self.on_vision_callback = None
        self.destination = destination
        self.timeout = timeout
        self.skt = SocketStateMachine(self.destination, self.timeout)
        self.ch = ExternalInterfacing(self._callback_handler)
        ready = threading.Barrier(2)
        self.es = ExternalSender(self.skt.get_socket(SOCKET_TYPE['Send']),
                                 ready, self.reconnect)
        self.er = ExternalReceiver(self.skt.get_socket(SOCKET_TYPE['Receive']),
                                   ready, self.ch.request, self.reconnect,
                                   self._send_alive_response)
        self.callback_switch = {
            1: self._callback_on_result_handler,
            2: self._callback_on_state_change_handler,
            3: self._callback_on_listen_handler,
            4: self._callback_on_vision_handler,
        }
        self.sync = {}
        self.sync_error = {}
        self._cancel_by_timeout = False

    @property
    def on_state_change_callback(self):
        with self._on_state_change_callback_lock:
            return self._on_state_change_callback

    @on_state_change_callback.setter
    def on_state_change_callback(self, callback_fun):
        with self._on_state_change_callback_lock:
            self._on_state_change_callback = callback_fun

    @on_state_change_callback.deleter
    def on_state_change_callback(self):
        with self._on_state_change_callback_lock:
            self._on_state_change_callback = None

    @property
    def on_result_callback(self):
        with self._on_result_callback_lock:
            return self._on_result_callback

    @on_result_callback.setter
    def on_result_callback(self, callback_fun):
        with self._on_result_callback_lock:
            self._on_result_callback = callback_fun

    @on_result_callback.deleter
    def on_result_callback(self):
        with self._on_result_callback_lock:
            self._on_result_callback = None

    @property
    def listen_callback(self):
        return self._listen_callback

    @listen_callback.setter
    def listen_callback(self, callback_fun):
        with self._listen_callback_lock:
            self._listen_callback = callback_fun

    @listen_callback.deleter
    def listen_callback(self):
        with self._listen_callback_lock:
            del self._listen_callback

    @property
    def on_vision_callback(self):
        return self._vision_callback

    @on_vision_callback.setter
    def on_vision_callback(self, callback_fun):
        with self._vision_callback_lock:
            self._vision_callback = callback_fun

    @on_vision_callback.deleter
    def on_vision_callback(self):
        with self._vision_callback_lock:
            del self._vision_callback

    def reconnect(self):
        print('reconnect ...')
        self.skt.set_state(
            SOCKET_TYPE['Send'],
            SOCKET_STATE['Disconnected'])
        self.skt.set_state(
            SOCKET_TYPE['Receive'],
            SOCKET_STATE['Disconnected'])
        self.es.stop()
        self.er.stop()
        self.skt.release()
        self.skt = SocketStateMachine(self.destination, self.timeout)
        ready = threading.Barrier(2)
        self.es = ExternalSender(self.skt.get_socket(SOCKET_TYPE['Send']),
                                 ready, self.reconnect)
        self.er = ExternalReceiver(self.skt.get_socket(SOCKET_TYPE['Receive']),
                                   ready, self.ch.request, self.reconnect,
                                   self._send_alive_response)

    def release(self):
        del self.on_state_change_callback
        del self.on_result_callback
        self._cancel_by_serial(0)
        print('cancel all completed')
        self.es.stop()
        self.er.stop()
        self.skt.release()

    def send_command(self, des, cmd, data, sync=False, timeout=None):
        packet, serial = get_packet(des, cmd, data)

        if self.skt.get_state(
                SOCKET_TYPE['Send']) != SOCKET_STATE['Connected']:
            if self.on_state_change_callback:
                print('send_command: sender not connected.')
                self.on_state_change_callback(
                    serial, cmd, error_code.COMMON_SOCKET_FAIL, 2)
            return serial, None

        self.es.request(packet)
        if sync:
            event = threading.Event()
            self.sync[serial] = event
            print('waiting command execute completed')

            if not event.wait(timeout):
                print(
                    'sync timeout, cancel command by serial:{}, cmd:{}'.format(
                        serial, cmd))
                if not self._cancel_by_timeout:
                    self._cancel_by_timeout = True
                    self._cancel_command(serial, cmd)
                self._cancel_by_timeout = False
            print('execute completed')
            return serial, self.sync_error.get(serial, None)
        else:
            return serial, None

    def _send_alive_response(self):
        self.es.request("KEEP_ALIVE_ACK")

    def _callback_handler(self, *args):
        # print('Receive:', args[0])
        try:
            recv = json.loads(args[0])
        except Exception as e:
            print('Exception:', args[0])
            raise e
        callback_type = recv.get("TYPE")
        self.callback_switch[callback_type](recv)

    def _callback_on_state_change_handler(self, kwargs):
        serial = kwargs.get("SERIAL", None)
        cmd = kwargs.get('CMD', None)
        error = kwargs.get("ERROR", None)
        state = kwargs.get("STATE", None)
        msg = 'onStateChange serial:{}, cmd:{}, error:{}, state:{}'
        print(msg.format(serial, cmd, error, STATE[state]))
        if self.sync.get(serial) and (1 < state <= 6 and state != 3):
            self.sync_error[serial] = {'state': state, 'error': error, }
            self.sync.pop(serial).set()
        if self.on_state_change_callback:
            self.on_state_change_callback(serial=serial, cmd=cmd, error=error, state=state)

    def _callback_on_result_handler(self, kwargs):
        serial = kwargs.get("SERIAL", None)
        cmd = kwargs.get('CMD', None)
        error = kwargs.get("ERROR", None)
        result = kwargs.get('RESULT', None)
        msg = 'onResult serial:{}, cmd:{}, error:{}, result:{}'
        print(msg.format(serial, cmd, error, result))
        if self.on_result_callback:
            self.on_result_callback(serial=serial, cmd=cmd, error=error, result=result)

    def _callback_on_listen_handler(self, kwargs):
        result = kwargs.get('RESULT', None)
        # msg = 'listen result:{}'
        # print(msg.format(result))
        if self.listen_callback:
            self.listen_callback(result)

    def _callback_on_vision_handler(self, kwargs):
        result = kwargs.get('RESULT', None)
        # msg = 'onVision serial:{}, cmd:{}, error:{}, result:{}'
        # print(msg.format(serial, cmd, error, result))
        if self.on_vision_callback:
            self.on_vision_callback(result)

    def _cancel_command(self, serial, cmd):
        args = {
            commands.VISION_REQUEST_DETECT_FACE: (
                DESTINATION["vision"],
                commands.VISION_CANCEL_DETECT_FACE,),
            commands.VISION_REQUEST_DETECT_PERSON: (
                DESTINATION["vision"],
                commands.VISION_CANCEL_DETECT_PERSON,),
            commands.VISION_REQUEST_RECOGNIZE_PERSON: (
                DESTINATION["vision"],
                commands.VISION_CANCEL_RECOGNIZE_PERSON,),
        }.get(cmd, serial)

        {
            commands.VISION_REQUEST_DETECT_FACE: self._cancel_by_cmd,
            commands.VISION_REQUEST_DETECT_PERSON: self._cancel_by_cmd,
            commands.VISION_REQUEST_RECOGNIZE_PERSON: self._cancel_by_cmd,
        }.get(cmd, self._cancel_by_serial)(args)

    def _cancel_by_cmd(self, args, sync=False, timeout=None):
        des, cmd = args
        data = {}
        serial, error = self.send_command(des, cmd, data, sync, timeout)
        return serial, error

    def _cancel_by_serial(self, serial, sync=True, timeout=5):
        des = DESTINATION["coordinator"]
        cmd = commands.CANCEL
        data = {
            'command': 0,
            'target_id': int(serial),
        }
        serial, error = self.send_command(des, cmd, data, sync, timeout)
        return serial, error


class ExternalSender(threading.Thread):
    """ """

    def __init__(self, skt, ready, recover_fun, **kwargs):
        super().__init__(**kwargs)
        self.setName('ExternalSender')
        self.daemon = True
        self.sock = skt
        # self.sock = socket.create_connection(destination, timeout)
        # self.destination = destination
        # self.timeout = timeout
        self._recover_fun = recover_fun
        self._ready = ready
        self.work_request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.start()

    def stop(self):
        self.work_request_queue.put(None)
        if self.sock:
            self.sock.close()

    def request(self, *args, **kwargs):
        """ call from other thread """
        self.work_request_queue.put((args, kwargs))
        return self.result_queue.get()

    def run(self):
        self._ready.wait()
        del self._ready
        print('ExternalSender', self.sock)
        while True:
            # a, k = self.work_request_queue.get()
            item = self.work_request_queue.get()
            if item is None:
                break
            a, k = item
            try:
                self.result_queue.put(self._send_message(self.sock, *a, **k))
            except ConnectionResetError:
                print('Server reset connection. Re-connect to server.')
                self.result_queue.put(None)
                self._recover_fun()
            self.work_request_queue.task_done()
        print('ExternalSender stop')

    @staticmethod
    def _send_message(sock, packet):
        if packet != "KEEP_ALIVE_ACK":
            print('send command')
        try:
            sock.sendall(packet.encode(encoding='utf-8'))
            sock.sendall('\n'.encode(encoding='utf-8'))
        except Exception as e:
            raise e
        # else:
        #     print('send message Done')


class ExternalReceiver(threading.Thread):
    """"""

    def __init__(
            self,
            skt,
            ready,
            external_callable,
            recover_fun,
            send_alive_response,
            **kwargs):
        super().__init__(**kwargs)
        self.setName('ExternalReceiver')
        self.daemon = True
        self.sock = skt
        self._recover_fun = recover_fun
        self._send_alive_response = send_alive_response
        # self.sock = socket.create_connection(destination, timeout)
        # self.destination = destination
        # self.timeout = timeout
        self._ready = ready
        self._external_callable = external_callable
        self._stop_event = threading.Event()
        self.start()

    def stop(self):
        self._stop_event.set()
        if self.sock:
            self.sock.close()
        print('ExternalReceiver stop')

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self._ready.wait()
        del self._ready
        print('ready receive message from ', self.sock)
        if_disconnect = False
        buf_size = 4096
        remaining_data = []
        while not self.stopped():
            try:
                if self.sock:
                    received = self.sock.recv(buf_size).decode(
                        'utf-8', errors='replace')
                else:
                    time.sleep(0.5)
                    received = ''
            except ConnectionAbortedError as e:
                # ignore
                print(e)
                break
            except OSError:
                if not self.stopped():
                    print('receiver not stopped')
                    raise
            except Exception:
                raise
            else:
                if not self.sock:
                    continue
                if not len(received):
                    if_disconnect = True
                    self._recover_fun()
                    break
                else:
                    if len(remaining_data):
                        remaining_data.append(received)
                        received = ''.join(remaining_data)
                        # print('remaining_data', remaining_data)
                        remaining_data.clear()
                    end = received.rfind('\n')
                    # '\n' not in received string end, i.e. not received full
                    # packet, only use completed packet, store not end packet
                    # in remaining date for next time receive data.
                    if end != len(received) - 1:
                        remaining_data.append(received[end + 1:])
                        # print(
                        # 'len > buf size, end:{}, len:{}, size:{}, received:{}, remaining:{} '.format(
                        # end, len(received), sys.getsizeof(received),
                        # received, remaining_data))
                    recv = received[0:end].splitlines()
                    [self._send_alive_response()
                     if 'KEEP_ALIVE_PROBE' == s else self._external_callable(s)
                     for s in recv if len(s) > 0]
        if not if_disconnect:
            print('receive message canceled')


class ExternalInterfacing(threading.Thread):
    """ """

    def __init__(self, external_callable, **kwargs):
        super().__init__(**kwargs)
        self.setName('ExternalInterfacing')
        self.daemon = True
        self.external_callable = external_callable
        self.work_request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.start()

    def request(self, *args, **kwargs):
        """ call from other thread """
        self.work_request_queue.put((args, kwargs))
        return self.result_queue.get()

    def run(self):
        while True:
            a, k = self.work_request_queue.get()
            self.result_queue.put(self.external_callable(*a, **k))
            self.work_request_queue.task_done()


class Serializer(threading.Thread):
    """ """

    def __init__(self, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.demon = True
        self.work_request_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.start()

    def apply(self, external_callable, *args, **kwargs):
        """ call from other thread """
        self.work_request_queue.put((external_callable, args, kwargs))
        return self.result_queue.get()

    def run(self):
        while True:
            external_callable, args, kwargs = self.work_request_queue.get()
            self.result_queue.put(external_callable(*args, **kwargs))
            self.work_request_queue.task_done()
