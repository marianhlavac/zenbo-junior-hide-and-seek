import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION


class PlayAction:
    DEFAULT_1 = 0
    DEFAULT_2 = 1
    NOD_1 = 2
    HEAD_UP_1 = 3
    HEAD_UP_2 = 4
    SHAKE_HEAD_1 = 5
    HEAD_UP_3 = 6
    HEAD_UP_4 = 7
    HEAD_DOWN_1 = 8
    HEAD_DOWN_2 = 9
    HEAD_DOWN_3 = 10
    SHAKE_HEAD_2 = 11
    HEAD_DOWN_4 = 12
    HEAD_UP_5 = 13
    HEAD_DOWN_5 = 14
    DANCE_B_1_LOOP = 15
    HEAD_UP_7 = 16
    MUSIC_1_LOOP = 17
    TURN_LEFT_1 = 18
    TURN_LEFT_2 = 19
    SHAKE_HEAD_3 = 20
    DANCE_S_1_LOOP = 21
    BODY_TWIST_1 = 22
    BODY_TWIST_2 = 23
    DANCE_2_LOOP = 24
    SHAKE_HEAD_4_LOOP = 25
    HEAD_TWIST_1_LOOP = 26
    DANCE_3_LOOP = 27
    SHAKE_HEAD_5 = 28
    SHAKE_HEAD_6 = 42
    HEAD_DOWN_7 = 43
    TURN_RIGHT_1 = 44
    TURN_RIGHT_2 = 45
    TURN_LEFT_REVERSE_1 = 46
    TURN_RIGHT_REVERSE_1 = 47
    TURN_LEFT_REVERSE_2 = 48
    TURN_RIGHT_REVERSE_2 = 49
    HEAD_UP_6 = 54


class Utility:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def play_action(self, number, sync=True, timeout=None):
        """
        Perform predefined actions by turning neck and wheels.
        Use PlayAction to set action number, naming with loop will be
        incessant replay. Use cancelCommandBySerial() or cancelCommandAll() to
        cancel action.

        :param number: number of predefined action
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOTION_PLAY_ACTION
        data = {
            'number': int(number),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def play_emotional_action(self, face, play_action, sync=True,
                              timeout=None):
        """
        Perform robot expression and predefined action.
        Use PlayAction to set action number, naming with loop will be
        incessant replay. Use cancelCommandBySerial() or cancelCommandAll() to
        cancel action.

        :param face: face expression ID
        :param play_action: action ID
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        cmd = commands.PLAY_EMOTIONAL_ACTION
        data = {
            'type': 8,
            'face': str(face),
            'number': int(play_action),
        }
        serial, error = self._inter_comm.send_command(
            DESTINATION["commander"], cmd, data)
        self._inter_comm.send_command(DESTINATION["coordinator"], cmd, data,
                                      sync, timeout)
        return serial, error

    def look_at_user(self, doa, sync=True, timeout=None):
        """
        Ask robot to look at user in robot front

        :param doa: direction of arrival
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_LOOK_AT_USER
        data = {
            'doa': float(doa),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def find_person_nearby(self, sync=True, timeout=None):
        """
        Ask robot to find person nearby

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_FIND_PERSON_NEARBY
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def track_face(self, enable_preview, large_preview, sync=False,
                   timeout=None):
        """
        Ask robot track the face.
        There are two "onResult" callback during trackFace processing:
        1. "TRACK_FACE_START_FIND_USER" : plugin start to find user
        2. "TRACK_FACE_FOUND_USER": plugin has found user, will start to follow

        :param enable_preview: set True to enable camera preview window for
            debug
        :param large_preview: set True to enable full screen preview,
            it works only when enablePreview is true
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_TRACK_FACE
        data = {
            'followingMode': False,
            'enablePreview': bool(enable_preview),
            'largePreview': bool(large_preview),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def follow_face(self, enable_preview, large_preview, sync=False,
                    timeout=None):
        """
        Ask robot follow the face.
        There are two "onResult" callback during followFace processing:
        1. "FOLLOW_FACE_START_FIND_USER": plugin start to find user
        2. "FOLLOW_FACE_FOUND_USER": plugin has found user, will start to
        follow

        :param enable_preview: set True to enable camera preview window for
            debug
        :param large_preview: set True to enable full screen preview,
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_TRACK_FACE
        data = {
            'followingMode': True,
            'enablePreview': bool(enable_preview),
            'largePreview': bool(large_preview),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def follow_object(self, sync=False, timeout=None):
        """
        Ask robot to follow object

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_FOLLOW_OBJECT
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error
