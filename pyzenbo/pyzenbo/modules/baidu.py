import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION


class Baidu:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def detect_face_from_photo(self, uri, sync=True, timeout=None):
        """
        Detect face from photo by Baidu AI,
        result is reported by onResult with key "RESULT".

        :param uri: photo URI in Zenbo
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_PROXY_BAIDU_DETECT_FACE_FROM_PHOTO
        data = {'uriString': str(uri)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def recognize_face_from_photo(
            self,
            uri,
            group_id='',
            sync=True,
            timeout=None):
        """
        Recognize face from photo by Baidu AI,
        result is reported by onResult with key "RESULT".

        :param uri: photo URI in Zenbo
        :param group_id: group ID for enroll setting, or set "" for
            default local device
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_PROXY_BAIDU_RECOGNIZE_FACE_FROM_PHOTO
        data = {'uriString': str(uri), 'groupId': str(group_id)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def recognize_text_from_photo(self, uri, sync=True, timeout=None):
        """
        Recognize text from photo by Baidu AI,
        result is reported by onResult with key "RESULT".

        :param uri: photo URI in Zenbo
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_PROXY_BAIDU_RECOGNIZE_TEXT_FROM_PHOTO
        data = {'uriString': str(uri)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error
