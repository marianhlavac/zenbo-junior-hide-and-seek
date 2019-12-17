import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION

BLINKING = 0x11
MARQUEE = 0x12
BREATHING = 0x13
CHARGING = 0x15
STOP = 0x14
AURA_STATIC = 0x20
AURA_BREATH = 0x21
AURA_STROBING = 0x22
AURA_COLOR_CYCLE = 0x23
AURA_RAINBOW = 0x24
AURA_BREATH_RAINBOW = 0x25
AURA_COMET = 0x26
AURA_RAINBOW_COMET = 0x27
AURA_MOVING_FLASH = 0x28
AURA_FLASH_DASH = 0x29
AURA_RAINBOW_WAVE = 0x2A
AURA_GLOWING_YOYO = 0x2B
AURA_STARRY_NIGHT = 0x2C
AURA_WAVE = 0x2D


class Lights:
    SYNC_BOTH = 0
    ASYNC_LEFT = 1
    ASYNC_RIGHT = 2


class Direction:
    DIRECTION_FORWARD = 0
    DIRECTION_BACKWARD = 1


class Speed:
    SPEED_DEFAULT = 0
    SPEED_SLOWER_1 = 1
    SPEED_SLOWER_2 = 2
    SPEED_FASTER_1 = -1
    SPEED_FASTER_2 = -2


class WheelLights:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def set_color(self, lights, active, color, sync=True, timeout=None):
        """
        Set the color of wheel LEDs.

        :param lights: wheel lights ID
        :param active: bitmap array of selected LED. bit7~bit0 corresponding
            LED7~LED0. Set the correspond bit to specify the selected LEDs.
            <br>In Zenbo junior, bit6~bit0 corresponding LED6~LED0.
            Set the correspond bit to specify the selected LEDs.
            Bit 7 is applied immediately: 1: applied immediately,
            0: applied on next pattern starting.
        :param color: color value in RGB format
            (e.g. RED is 0x00ff0000, GREEN is 0x0000ff00, BLUE is 0x000000ff)
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_COLOR
        data = {
            'id': int(lights),
            'active': int(active),
            'color': int(color),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_static(self, lights, sync=True, timeout=None):
        """
        Start the static pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_STATIC,
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_strobing(self, lights, speed, sync=True, timeout=None):
        """
        Start the strobing pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_STROBING,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_breath(self, lights, speed, sync=True, timeout=None):
        """
        Start the breath pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_BREATH,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_color_cycle(self, lights, speed, sync=True, timeout=None):
        """
        Start the color cycle pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_COLOR_CYCLE,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_rainbow(self, lights, direction, speed, sync=True, timeout=None):
        """
        Start the rainbow pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_RAINBOW,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_breath_rainbow(self, lights, speed, sync=True, timeout=None):
        """
        Start the breath rainbow pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_BREATH_RAINBOW,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_comet(self, lights, direction, speed, sync=True, timeout=None):
        """
        Start the comet pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_COMET,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_rainbow_comet(self, lights, direction, speed, sync=True,
                            timeout=None):
        """
        Start the rainbow comet pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_RAINBOW_COMET,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_moving_flash(self, lights, direction, speed, sync=True,
                           timeout=None):
        """
        Start the moving flash pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_MOVING_FLASH,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_flash_dash(self, lights, direction, speed, sync=True,
                         timeout=None):
        """
        Start the flash dash pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_FLASH_DASH,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_rainbow_wave(self, lights, direction, speed, sync=True,
                           timeout=None):
        """
        Start the rainbow wave pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param direction: forward or backward
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_RAINBOW_WAVE,
            't1': int(speed),
            'direction': int(direction),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_glowing_yoyo(self, lights, speed, sync=True, timeout=None):
        """
        Start the glowing yoyo pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_GLOWING_YOYO,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_starry_night(self, lights, speed, sync=True, timeout=None):
        """
        Start the starry night pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_STARRY_NIGHT,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def start_wave(self, lights, speed, sync=True, timeout=None):
        """
        Start the wave pattern action. Only support in Zenbo junior.

        :param lights: wheel lights ID
        :param speed: speed level
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_SET_PATTERN
        data = {
            'id': int(lights),
            'pattern': AURA_WAVE,
            't1': int(speed),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def turn_off(self, lights, sync=True, timeout=None):
        """
        Stop the pattern set by startPattern.

        :param lights: wheel lights ID
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["coordinator"]
        cmd = commands.WHEEL_LIGHTS_STOP_PATTEN
        data = {
            'id': int(lights),
            'active': 0,
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error
