import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION
from pyzenbo.modules.wait_for import WaitForResult

CAPACITY_TOUCH_EVENT_ALL = 0  # receive all event type
CAPACITY_TOUCH_EVENT_VERY_SHORT = 1  # 0.35 sec. > touch time >= 0.005 sec.
CAPACITY_TOUCH_EVENT_SHORT = 2  # 1 sec. > touch time >= 0.35 sec.
CAPACITY_TOUCH_EVENT_MEDIUM = 3  # 3 sec. > touch time >= 1 sec.
CAPACITY_TOUCH_EVENT_LONG = 4  # touch time > 3 sec.

SONAR_POSITION_FR = 0
SONAR_POSITION_FL = 1
SONAR_POSITION_FC = 2

OPERATOR_EQUAL = 0
OPERATOR_NOT_EQUAL = 1
OPERATOR_MORE_THAN = 2
OPERATOR_LESS_THAN = 3
OPERATOR_MORE_THAN_OR_EQUAL = 4
OPERATOR_LESS_THAN_OR_EQUAL = 5


class Sensor:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def register_capacity_touch_sensor_event(self, event_type=0,
                                             sync=True, timeout=None):
        """
        Register the capacity touch sensor event callback.

        :param event_type: event type 1 to 4, 0 means receive all event
            0: receive all event type
            1: 0.35 sec. > touch time ≥ 0.005 sec.
            2: 1 sec. > touch time ≥ 0.35 sec.
            3: 3 sec. > touch time ≥ 1 sec.
            4: touch time > 3 sec.
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_CAPACITY_TOUCH_EVENT_REGISTER
        event_type = int(event_type) if 0 <= int(event_type) <= 4 else 0
        data = {'event_type': event_type}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_capacity_touch_sensor_event(self, event_type=0,
                                               sync=True, timeout=None):
        """
        Unregister the capacity touch sensor event callback.

        :param event_type: event type 1 to 4, 0 means receive all event
            0: receive all event type
            1: 0.35 sec. > touch time ≥ 0.005 sec.
            2: 1 sec. > touch time ≥ 0.35 sec.
            3: 3 sec. > touch time ≥ 1 sec.
            4: touch time > 3 sec.
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_CAPACITY_TOUCH_EVENT_UNREGISTER
        event_type = int(event_type) if 0 <= int(event_type) <= 4 else 0
        data = {'event_type': event_type}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def wait_for_capacity_touch_sensor_event(self, event_type=0, timeout=10):
        """
        Wait for capacity touch event occur and return sensor result.

        :param event_type: event type 1 to 4, 0 means receive all event
            0: receive all event type
            1: 0.35 sec. > touch time ≥ 0.005 sec.
            2: 1 sec. > touch time ≥ 0.35 sec.
            3: 3 sec. > touch time ≥ 1 sec.
            4: touch time > 3 sec.
        :param timeout: maximum blocking time in second, None means infinity
        :return: sensor result, if timeout will return None
        """
        serial, result = self.register_capacity_touch_sensor_event(event_type)
        # if register command state is SUCCEED
        if result is not None and result['state'] is 5:
            print('wait for capacity touch start')
            wait_for = WaitForResult(self._inter_comm)
            wait_for_result = wait_for.start(
                timeout, commands.SENSOR_CAPACITY_TOUCH_EVENT_REGISTER)
            self.unregister_capacity_touch_sensor_event(event_type)
            return wait_for_result
        else:
            print('register capacity touch start fail serial:',
                  serial, 'result:', result)

    def get_sonar(self, position, sync=True, timeout=None):
        """
        Get sonar sensor value.

        :param position: sonar position
            0: front right
            1: front left
            2 :front center
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_SONAR_GET
        data = {'position': int(position) if 0 <= int(position) <= 2 else 0}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def register_sonar(self, position, interval=0.5, sync=True, timeout=None):
        """
        Register the sonar sensor callback.

        :param position: sonar position
            0: front right
            1: front left
            2 :front center
        :param interval: callback interval accept only positive numeric
            in seconds, default and minimum value is 0.5 second
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_SONAR_REGISTER
        data = {
            'position': int(position) if 0 <= int(position) <= 2 else 0,
            'interval': float(interval) if 0.5 <= float(interval) else 0.5}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_sonar(self, position, sync=True, timeout=None):
        """
        Unregister the sonar sensor callback.

        :param position: sonar position
            0: front right
            1: front left
            2 :front center
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_SONAR_UNREGISTER
        data = {'position': int(position) if 0 <= int(position) <= 2 else 0}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def register_sonar_event(self, position, operator, value,
                             sync=True, timeout=None):
        """
        Register the sonar sensor event callback, when sensor reach the
        condition that specified, the result is returned by on_result_callback.

        :param position: sonar position
            0: front right
            1: front left
            2 :front center
        :param operator: comparison type with a threshold value.
            0: = (Equal)
            1: ≠ (Not Equal)
            2: > (Greater Than)
            3: ≥ (Greater Than or Equal To)
            4: < (Less Than)
            5: ≤ (Less Than or Equal To)
        :param value: threshold value to compare sensor data
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_SONAR_EVENT_REGISTER
        data = {
            'position': int(position) if 0 <= int(position) <= 2 else 0,
            'operator': int(operator),
            'value': float(value)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_sonar_event(self, position, operator, value,
                               sync=True, timeout=None):
        """
        Unregister the sonar sensor event callback.

        :param position: sonar position
            0: front right
            1: front left
            2 :front center
        :param operator: comparison type with a threshold value.
            0: = (Equal)
            1: ≠ (Not Equal)
            2: > (Greater Than)
            3: ≥ (Greater Than or Equal To)
            4: < (Less Than)
            5: ≤ (Less Than or Equal To)
        :param value: threshold value to compare sensor data
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_SONAR_EVENT_UNREGISTER
        data = {
            'position': int(position) if 0 <= int(position) <= 2 else 0,
            'operator': int(operator),
            'value': float(value)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def get_neck_encoder(self, sync=True, timeout=None):
        """
        Get neck encoder value.

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_NECK_ENCODER_GET
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def register_neck_encoder(self, interval=0.5, sync=True, timeout=None):
        """
        Register the neck encoder callback.

        :param interval: callback interval accept only positive numeric
            in seconds, default and minimum value is 0.5 second
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_NECK_ENCODER_REGISTER
        data = {'interval': float(interval) if 0.5 <= float(interval) else 0.5}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_neck_encoder(self, sync=True, timeout=None):
        """
        Unregister the neck encoder callback.

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_NECK_ENCODER_UNREGISTER
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def register_neck_encoder_event(self, operator, value,
                                    sync=True, timeout=None):
        """
        Register the neck encoder event callback, when neck encoder reach the
        condition that specified, the result is returned by on_result_callback.

        :param operator: comparison type with a threshold  value.
            0: = (Equal)
            1: ≠ (Not Equal)
            2: > (Greater Than)
            3: ≥ (Greater Than or Equal To)
            4: < (Less Than)
            5: ≤ (Less Than or Equal To)
        :param value: threshold value to compare sensor data
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_NECK_ENCODER_EVENT_REGISTER
        data = {'operator': int(operator), 'value': float(value)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_neck_encoder_event(self, operator, value,
                                      sync=True, timeout=None):
        """
        Unregister the neck encoder event callback.

        :param operator: comparison type with a threshold value.
            0: = (Equal)
            1: ≠ (Not Equal)
            2: > (Greater Than)
            3: ≥ (Greater Than or Equal To)
            4: < (Less Than)
            5: ≤ (Less Than or Equal To)
        :param value: threshold value to compare sensor data
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_NECK_ENCODER_EVENT_UNREGISTER
        data = {'operator': int(operator), 'value': float(value)}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def register_trigger_key_event(self, sync=True, timeout=None):
        """
        Register the trigger key event callback.

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_TRIGGER_KEY_EVENT_REGISTER
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def unregister_trigger_key_event(self, sync=True, timeout=None):
        """
        Unregister the trigger key event callback.

        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION['sensor']
        cmd = commands.SENSOR_TRIGGER_KEY_EVENT_UNREGISTER
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def wait_for_trigger_key_event(self, timeout=10):
        """
        Wait for trigger key event occur and return sensor result.

        :param timeout: maximum blocking time in second, None means infinity
        :return: sensor result, if timeout will return None
        """
        serial, result = self.register_trigger_key_event()
        # if register command state is SUCCEED
        if result is not None and result['state'] is 5:
            print('wait for trigger key start')
            wait_for = WaitForResult(self._inter_comm)
            wait_for_result = wait_for.start(
                timeout, commands.SENSOR_TRIGGER_KEY_EVENT_REGISTER)
            self.unregister_trigger_key_event()
            return wait_for_result
        else:
            print('register trigger key start fail serial:',
                  serial, 'result:', result)
