import threading

from pyzenbo.modules.zenbo_command import VISION_REQUEST_DETECT_FACE, VISION_REQUEST_RECOGNIZE_PERSON


class BaseWaitFor:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

        self.origin_on_state_change = self._inter_comm.on_state_change_callback
        self.origin_on_result = self._inter_comm.on_result_callback
        self.origin_listen = self._inter_comm.listen_callback
        self.origin_on_vision_callback = self._inter_comm.on_vision_callback

        self._inter_comm.on_state_change_callback = self._on_state_change_dispatch
        self._inter_comm.on_result_callback = self._on_result_dispatch
        self._inter_comm.listen_callback = self._listen_dispatch
        self._inter_comm.on_vision_callback = self._vision_dispatch

    def _on_state_change_handler(self, **kwargs):
        pass

    def _on_result_handler(self, **kwargs):
        pass

    def _listen_handler(self, args):
        pass

    def _vision_handler(self, args):
        pass

    def _on_state_change_dispatch(self, **kwargs):
        self._on_state_change_handler(**kwargs)
        if self.origin_on_state_change:
            self.origin_on_state_change(**kwargs)

    def _on_result_dispatch(self, **kwargs):
        self._on_result_handler(**kwargs)
        if self.origin_on_result:
            self.origin_on_result(**kwargs)

    def _listen_dispatch(self, args):
        self._listen_handler(args)
        if self.origin_listen:
            self.origin_listen(args)

    def _vision_dispatch(self, args):
        self._vision_handler(args)
        if self.origin_on_vision_callback:
            self.origin_on_vision_callback(args)

    def _restore_callback(self):
        self._inter_comm.on_state_change_callback = self.origin_on_state_change
        self._inter_comm.on_result_callback = self.origin_on_result
        self._inter_comm.listen_callback = self.origin_listen
        self._inter_comm.on_vision_callback = self.origin_on_vision_callback


class WaitForListen(BaseWaitFor):
    def __init__(self, inter_comm):
        super().__init__(inter_comm)
        self.event_slu = threading.Event()
        self.slu_result = None

    def _listen_handler(self, args):
        slu = args.get('event_slu_query', None)
        if slu:
            utterance = slu.get('user_utterance', None)
            if utterance:
                self.slu_result = slu
                self.event_slu.set()

    def start(self, timeout):
        self.event_slu.wait(timeout)
        self._restore_callback()
        return self.slu_result


class WaitForDetectFace(BaseWaitFor):
    def __init__(self, inter_comm):
        super().__init__(inter_comm)
        self.event_detected = threading.Event()
        self.result = None

    def _on_state_change_handler(self, **kwargs):
        state = kwargs.get('state')
        if kwargs.get('cmd') != VISION_REQUEST_DETECT_FACE:
            return
        # if state is ACTIVE
        if state == 3:
            print('wait for detect face start')
            return
        else:
            print('detect face start fail', kwargs)
            if not self.event_detected.isSet():
                self.result = kwargs
                self.event_detected.set()

    def _vision_handler(self, args):
        if not self.event_detected.isSet():
            self.result = args
            self.event_detected.set()

    def start(self, timeout):
        if not self.event_detected.wait(timeout):
            print('wait for detect face timeout')
        self._restore_callback()
        return self.result


class WaitForRecognizeFace(BaseWaitFor):
    def __init__(self, inter_comm):
        super().__init__(inter_comm)
        self.event_detected = threading.Event()
        self.result = None
        self.user_id = None

    def _on_state_change_handler(self, **kwargs):
        state = kwargs.get('state')
        if kwargs.get('cmd') != VISION_REQUEST_RECOGNIZE_PERSON:
            return
        # if state is ACTIVE
        if state == 3:
            print('wait for recognize face start')
            return
        else:
            print('detect recognize start fail', kwargs)
            if not self.event_detected.isSet():
                self.result = kwargs
                self.event_detected.set()

    def _vision_handler(self, args):
        if self.user_id is None and not self.event_detected.isSet():
            self.result = args
            self.event_detected.set()
            return
        for arg in args:
            uuid = arg.get('context').get('nameValuePairs').get('uuid')
            if uuid == self.user_id and not self.event_detected.isSet():
                self.result = args
                self.event_detected.set()

    def start(self, user_id, timeout):
        self.user_id = user_id
        if not self.event_detected.wait(timeout):
            print('wait for recognize face timeout')
        self._restore_callback()
        return self.result


class WaitForResult(BaseWaitFor):
    def __init__(self, inter_comm):
        super().__init__(inter_comm)
        self.event = threading.Event()
        self.result = None
        self.cmd = None

    def _on_result_handler(self, **kwargs):
        if self.cmd is not None and kwargs.get('cmd') != self.cmd:
            return
        result = kwargs.get('result')
        if result is not None and not self.event.isSet():
            self.result = result
            self.event.set()

    def start(self, timeout, cmd):
        self.cmd = cmd
        if not self.event.wait(timeout):
            print('wait for result timeout')
        self._restore_callback()
        return self.result
