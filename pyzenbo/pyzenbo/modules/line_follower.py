import json

import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules import error_code
from pyzenbo.modules.inter_communication import DESTINATION


class LineFollowerConfig:
    COLOR = {
        'UNKNOWN': -1,
        'BLACK': 0,
        'WHITE': 1,
        'RED': 2,
        'YELLOW': 3,
        'GREEN': 4,
        'BLUE': 5,
    }

    BEHAVIOR = {
        'UNKNOWN': -1,
        'NOTHING': 0,
        'TERMINATE': 1,
        'U_TURN': 2,
        'FORKED_LEFT': 3,
        'FORKED_RIGHT': 4,
        'CROSSROAD_LEFT': 5,
        'CROSSROAD_RIGHT': 6,
        'SPEED_LEVEL': 7,
        'ROTATION': 8,
        'CURVE': 9,
    }

    SPEED = {
        'L1': 1,
        'L2': 2,
        'L3': 3,
    }

    _rule_list = {}

    def add_rule(self, color, behavior, *args):
        """
        Change the configuration of line following.

        :param color: COLOR.BLACK can only support the settings of
             BEHAVIOR.SPEED_LEVEL
        :param behavior: The default settings of the configuration is
            BEHAVIOR.NOTHING. Can't change the setting of BEHAVIOR.UNKNOWN
        :param args: The settings of BEHAVIOR.SPEED_LEVEL and BEHAVIOR.ROTATION
            require third parameter,  BEHAVIOR.SPEED_LEVEL require SPEED.
            The settings of BEHAVIOR.ROTATION require inputting rotational
            angle (in degree)
        :return: Return error_code.NO_ERROR if successfully change the
            settings. Otherwise, it will return a certain error code.
        """
        ret = self._accept_color(color, behavior)
        if ret != error_code.NO_ERROR:
            return ret
        return self._check_rule(color, behavior, args)

    def remove_rule(self, color):
        """
        Remove the settings of specific color.

        :param color: specific color
        """
        del self._rule_list[str(color)]

    def get_rule(self, color):
        """
        Return the settings of specific color.

        :param color: specific color
        :return: Return color rule for specific color.
            Otherwise, it will return None if the color doesn't have any
            settings.
        """
        return self._rule_list.get(str(color))

    def get_rule_list(self):
        """
        Get the configuration list.

        :return: Return a new configuration list, which is a shallow copy of
            the old one
        """
        return self._rule_list.copy()

    def build(self):
        """
        Returns a string that representing the configuration.

        :return:a JSON string that representing the configuration
        """
        return json.dumps(self._rule_list)

    def _accept_color(self, color, behavior):
        if isinstance(color, int):
            if color == 2 or 4 <= color <= 5:
                return error_code.NO_ERROR
            elif color == 0 and behavior == self.BEHAVIOR['SPEED_LEVEL']:
                return error_code.NO_ERROR
            else:
                return error_code.LINE_FOLLOWER_INVALID_COLOR_TYPE
        elif isinstance(color, list):
            if 0 <= len(color) > 4:
                return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
            if color[0] != self.COLOR['YELLOW'] or color.count(
                    self.COLOR['YELLOW'] > 1):
                return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
            perv = self.COLOR['UNKNOWN']
            invalid = {
                self.COLOR['RED']: False,
                self.COLOR['GREEN']: False,
                self.COLOR['BLUE']: False,
            }
            for c in color[1:]:
                if invalid.get(c, True) or c == perv:
                    return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
                perv = c
            return error_code.NO_ERROR
        else:
            return error_code.LINE_FOLLOWER_INVALID_COLOR_TYPE

    def _check_rule(self, color, behavior, args):
        if not (0 <= behavior <= 9):
            return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
        if behavior == self.BEHAVIOR['SPEED_LEVEL']:
            if len(args) == 0 or not (1 <= args[0] <= 3):
                return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
            self._rule_list[str(color)] = {behavior: args[0]}
            return error_code.NO_ERROR
        elif behavior == self.BEHAVIOR['ROTATION']:
            if len(args) == 0:
                return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
            try:
                angle = float(args[0])
            except ValueError as e:
                print(e)
                return error_code.LINE_FOLLOWER_INVALID_ARGUMENT
            self._rule_list[str(color)] = {behavior: angle}
            return error_code.NO_ERROR
        else:
            self._rule_list[str(color)] = behavior
            return error_code.NO_ERROR


class LineFollower:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def calibrate(self, reset=False, sync=True, timeout=None):
        """
        Run calibration for line sensor.

        :param reset: True for reset to default RGB value
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_LINE_FOLLOWER_COLOR_CALIBRATE
        data = {
            'value': -1 if reset else 0,
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def demo(self, sync=False, timeout=None):
        """
        Start line following with default configuration patterns.
        Default pattern config as bellow:
        G-R-G: stop,
        B-R-B: turn left,
        B-G-B: turn right,
        G-B-G: turn around,
        R-G-R: go straight,
        R-B-R: speed up,
        G-R-B: slow down,
        B-R-G: normal speed

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_DEMO_LINE_FOLLOWER
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def get_color(self, sync=True, timeout=None):
        """
        Return RGB values in order to get which color it is
        (Black, White, Red, Green, Blue, Yellow)
        RGB values will be returned as JSON string of onResult() with the
        bundle key of "Color_Result".

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_LINE_FOLLOWER_COLOR_IDENTIFICATION
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def follow_line(self, json_string=None, sync=True, timeout=None):
        """
        Start line following by using customize configuration.
        If line color or pattern is changed, result will be returned in JSON
        string of with the bundle key Color_Result" and "Pattern_Result".

        :param json_string: configuration in JSON string type, can build by
            LineFollowerConfig
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.UTILITY_LINE_FOLLOWER
        if json_string is None:
            config = LineFollowerConfig()
            config.add_rule(
                LineFollowerConfig.COLOR['BLACK'],
                LineFollowerConfig.BEHAVIOR['SPEED_LEVEL'],
                LineFollowerConfig.SPEED['L2'])
            json_string = config.build()
        data = {'string': str(json_string)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def update_config(self, serial, json_string, sync=True, timeout=None):
        """
        Update configuration during line following.

        :param serial: The serial number during line following
        :param json_string: configuration in JSON string type, can build by
            LineFollowerConfig
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['system']
        cmd = commands.UTILITY_SEND_INFO
        data = {
            'TARGET': int(serial),
            'INFO': {'arguments': {'string': str(json_string)}},
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def set_behavior(self, serial, behavior, arg=None, sync=True,
                     timeout=None):
        """
        Set behavior immediately during line following.

        :param serial: The serial number during line following
        :param behavior: The default settings of the configuration is
            BEHAVIOR.NOTHING, Can't change the setting of BEHAVIOR.UNKNOWN
        :param arg: The settings of BEHAVIOR.SPEED_LEVEL and BEHAVIOR.ROTATION
            The settings of BEHAVIOR.SPEED_LEVEL require third parameter SPEED
            and the settings of BEHAVIOR.ROTATION requires inputting rotational
            angle (in degree).
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['system']
        cmd = commands.UTILITY_SEND_INFO
        config = LineFollowerConfig()
        config.add_rule(LineFollowerConfig.COLOR['RED'],
                        behavior, arg)
        values = config.get_rule(LineFollowerConfig.COLOR['RED'])
        data = {
            'TARGET': int(serial),
            'INFO': {'setBehavior': {'string': {'behavior': values}}},
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error
