import math

import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION


class Motion:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def move_body(self, relative_x=0, relative_y=0, relative_theta_degree=0,
                  speed_level=0, sync=True, timeout=None):
        """
        Move body to a new location and turn head to a new angle relative to
        original pose with specified speed level.

        :param relative_x: relative distance (in meters) in x-axis direction,
            positive value would go forward
        :param relative_y: relative distance (in meters) in y-axis direction,
            positive value would go right
        :param relative_theta_degree: relative rotational angle (in degree)
        :param speed_level: speed level from 1 to 6, 1 is slowest, and 6 is
            fastest
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOTION_MOVE_BODY
        data = {
            'iRelX': float(relative_x),
            'iRelY': float(relative_y),
            'iRelTheta': math.radians(relative_theta_degree),
            'time': int(speed_level) if 0 < speed_level <= 6 else 0,
            'mode': 2 if 0 < speed_level <= 6 else 0,
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def move_head(self, yaw_degree=0, pitch_degree=0, speed_level=1,
                  sync=True, timeout=None):
        """
        Ask robot to turn its head, use SpeedLevel.Head to control moving
        speed.

        :param yaw_degree: the angle in degrees, the range is -45(left) to
            45(right) In Zenbo junior is not effect
        :param pitch_degree: the angle in degrees, the range is -15(down) to
            55(up) In Zenbo junior the range is -10(down) to 50(up)
        :param speed_level: speed level from 1 to 3, 1 is slowest, and 3 is
            fastest
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOVE_HEAD
        data = {
            'yawAngle': math.radians(yaw_degree),
            'pitchAngle': math.radians(pitch_degree),
            'yawTime': int(speed_level) if 0 < speed_level <= 3 else 1,
            'pitchTime': int(speed_level) if 0 < speed_level <= 3 else 1,
            'mode': 2,
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def stop_moving(self, sync=True, timeout=None):
        """
        Stop robot's movement in motion subclass, including neck and body.

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOTION_STOP
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def remote_control_body(self, direction, sync=True, timeout=None):
        """
        Control body to move until remoteControlBody(STOP) or
        stopMoving() command is received.

        :param direction: STOP=0, FORWARD=1, BACKWARD=2, TURN_LEFT=3,
            TURN_RIGHT=4
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOTION_REMOTE_CONTROL_BODY_STOP if direction == 0 \
            else commands.MOTION_REMOTE_CONTROL_BODY
        data = {
            'number': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def remote_control_head(self, direction, sync=True, timeout=None):
        """
        Control head to move until remoteControlHead(STOP) or
        stopMoving() command is received. The limit of pitch is -15 ~ 55
        degrees, and the limit of yaw is -45 ~ 45 degrees.

        :param direction: STOP=0, UP=1, DOWN=2, LEFT=3, RIGHT=4
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.MOTION_REMOTE_CONTROL_HEAD_STOP if direction == 0 \
            else commands.MOTION_REMOTE_CONTROL_HEAD
        data = {
            'number': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error
