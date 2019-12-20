import pyzenbo

def _on_state_change_callback(serial, cmd, error_code, state):
    print('State change: serial: {}, cmd: {}, error_code: {}, state: {}'.format(serial, cmd, error_code, state))

def connect_robot(ip) -> pyzenbo.PyZenbo:
    print('Connecting to the robot ({})...'.format(ip))
    return pyzenbo.connect(ip, _on_state_change_callback)