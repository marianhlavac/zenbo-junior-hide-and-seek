import threading

import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace
from pyzenbo.modules.error_code import code_to_description

host = '192.168.0.186'
sdk = pyzenbo.connect(host)
domain = 'E7AABB554ACB414C9AB9BF45E7FA8AD9'
timeout = 15
is_looping = True


def on_state_change(serial, cmd, error, state):
    msg = 'on_state_change serial:{}, cmd:{}, error:{}, state:{}'
    print(msg.format(serial, cmd, error, state))
    if error:
        print('on_state_change error:', code_to_description(error))


def on_result(**kwargs):
    print('on_result', kwargs)


def on_vision(*args):
    print('on_vision', args)
    if not event_vision.isSet():
        event_vision.set()


def listen_callback(args):
    slu = args.get('event_slu_query', None)
    if slu:
        print(slu)
        if not event_listen.isSet():
            event_listen.set()


def say_hello_and_ask():
    print('say_hello_and_ask')
    sdk.robot.set_expression(RobotFace.HAPPY, timeout=5)
    sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    sdk.robot.speak('Hello, my name is Zenbo Junior. Nice to meet you.')
    sdk.robot.speak_and_listen('Which city do you like? You can say Hello Block City, or Hello White City')


def not_found():
    print('not_found')
    sdk.robot.set_expression(RobotFace.TIRED, timeout=5)
    sdk.robot.speak('No one is here')


event_vision = threading.Event()
event_listen = threading.Event()
sdk.on_state_change_callback = on_state_change
sdk.on_result_callback = on_result
sdk.on_vision_callback = on_vision
sdk.robot.register_listen_callback(domain, listen_callback)
sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)

try:
    while is_looping:
        result = sdk.vision.request_detect_face(enable_debug_preview=True, timeout=50)
        print(result)
        is_detect_face = event_vision.wait(timeout)
        sdk.vision.cancel_detect_face()
        if is_detect_face:
            say_hello_and_ask()
            is_get_listening = event_listen.wait(timeout)
        else:
            not_found()
        sdk.robot.set_expression(RobotFace.HIDEFACE, timeout=5)
finally:
    sdk.robot.stop_speak_and_listen()
    sdk.vision.cancel_detect_face()
    sdk.release()
