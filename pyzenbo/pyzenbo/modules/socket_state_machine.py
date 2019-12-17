import socket
import time

SOCKET_STATE = {
    'Init': 0,
    'Connected': 1,
    'Disconnected': 2,
    'Retry_1': 3,
    'Retry_2': 4,
    'Retry_3': 5,
    'Failed': 6,
    'Closed': 7}
SOCKET_TYPE = {
    'Send': 0,
    'Receive': 1}


class SocketStateMachine:

    def __init__(self, destination, timeout=2):
        self.destination = destination
        self.timeout = timeout
        self.stateSend = SOCKET_STATE['Init']
        self.stateReceive = SOCKET_STATE['Init']
        self.socketSend = self._connect(SOCKET_TYPE['Send'])
        if self.socketSend:
            self.socketReceive = self._connect(SOCKET_TYPE['Receive'])
            if not self.socketReceive:
                self._fail()
        else:
            self.socketReceive = None
            self._fail()

    def get_socket(self, socket_type):
        if socket_type == SOCKET_TYPE['Send']:
            return self.socketSend
        if socket_type == SOCKET_TYPE['Receive']:
            return self.socketReceive

    def get_state(self, socket_type):
        if socket_type == SOCKET_TYPE['Send']:
            return self.stateSend
        if socket_type == SOCKET_TYPE['Receive']:
            return self.stateReceive

    def set_state(self, socket_type, state):
        print('set socket %d state to %d' % (socket_type, state))
        if socket_type == SOCKET_TYPE['Send']:
            self.stateSend = state
        if socket_type == SOCKET_TYPE['Receive']:
            self.stateReceive = state

    def _connect(self, socket_type):
        print('socket %d start connect' % socket_type)
        fail_state_transform = {
            SOCKET_STATE['Init']: SOCKET_STATE['Retry_1'],
            SOCKET_STATE['Disconnected']: SOCKET_STATE['Retry_1'],
            SOCKET_STATE['Retry_1']: SOCKET_STATE['Retry_2'],
            SOCKET_STATE['Retry_2']: SOCKET_STATE['Retry_3'],
            SOCKET_STATE['Retry_3']: SOCKET_STATE['Failed'],
        }

        sk = None
        while self.get_state(socket_type) != SOCKET_STATE['Connected'] and \
                self.get_state(socket_type) != SOCKET_STATE['Failed']:
            try:
                if self.get_state(socket_type) != SOCKET_STATE['Init'] and \
                        self.get_state(socket_type) != SOCKET_STATE['Disconnected']:
                    time.sleep(1)
                if socket_type == SOCKET_TYPE['Send']:
                    sk = socket.create_connection(
                        self.destination, self.timeout)
                if socket_type == SOCKET_TYPE['Receive']:
                    sk = socket.create_connection(
                        self.destination)
                self.set_state(socket_type, SOCKET_STATE['Connected'])
            except (TimeoutError, socket.timeout) as e:
                sk = None
                print('socket(%d) connect time out! state = %d' %
                      (socket_type, self.get_state(socket_type)))
                self.set_state(
                    socket_type, fail_state_transform.get(
                        self.get_state(socket_type)))
            except ConnectionRefusedError as e:
                sk = None
                print('socket(%d) connect refused! state = %d' %
                      (socket_type, self.get_state(socket_type)))
                self.set_state(
                    socket_type, fail_state_transform.get(
                        self.get_state(socket_type)))
        return sk

    def release(self):
        if self.socketSend:
            self.socketSend.close()
            self.socketSend = None
            self.set_state(SOCKET_TYPE['Send'], SOCKET_STATE['Closed'])
        if self.socketReceive:
            self.socketReceive.close()
            self.socketReceive = None
            self.set_state(SOCKET_TYPE['Receive'], SOCKET_STATE['Closed'])

    def _fail(self):
        if self.socketSend:
            self.socketSend.close()
            self.socketSend = None
            self.set_state(SOCKET_TYPE['Send'], SOCKET_STATE['Failed'])
        if self.socketReceive:
            self.socketReceive.close()
            self.socketReceive = None
            self.set_state(SOCKET_TYPE['Receive'], SOCKET_STATE['Failed'])
