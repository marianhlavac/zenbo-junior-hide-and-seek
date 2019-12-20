import pyzenbo

def on_state_change(serial, cmd, error, state):
    msg = 'on_state_change serial:{}, cmd:{}, error:{}, state:{}'
    print(msg.format(serial, cmd, error, state))

def connect_robot(ip) -> pyzenbo.PyZenbo:
    print('Connecting to the robot ({})...'.format(ip))
    return pyzenbo.connect(ip, on_state_change)