import ast
import asyncio
import time
import unittest

# from context import pyzenbo
import pyzenbo
from pyzenbo import LineFollowerConfig
from pyzenbo import error_code
from pyzenbo import zenbo_command

WHEEL_LIGHT_TEST_DELAY = 10
UTILITY_TEST_DELAY = 10

host = '192.168.0.214'

sdk = pyzenbo.connect(host)


def on_state_change(serial, cmd, error, state):
    msg = 'on_state_change serial:{}, cmd:{}, error:{}, state:{}'
    print(msg.format(serial, cmd, error, state))
    if error:
        print('on_state_change error:', error_code.code_to_description(error))


def on_result(**kwargs):
    print('on_result', kwargs)


def listen(args):
    utterance = args.get('event_user_utterance', None)
    vad = args.get('event_vad_status', None)
    slu = args.get('event_slu_query', None)
    msg = 'listen uu:{}, vad:{}, slu:{}'
    print(msg.format(utterance, vad, slu))
    if not utterance and not vad and not slu:
        print('listen raw:{}'.format(args))
    result = parser_listen_result(slu)
    if result is not None:
        print('slu_result:{}'.format(result))


def parser_listen_result(slu):
    if slu is None:
        return
    utterance = slu.get('user_utterance', None)
    if utterance is None:
        return
    utterance = ast.literal_eval(utterance)
    result = utterance[0].get('result', None)
    if result is None:
        return
    return result[0]


def vision(args):
    print('vision', args)


def delay_for_release(delay):
    async def do_delay_release(future):
        await asyncio.sleep(delay)
        print("delay for release")
        return future()

    loop = asyncio.get_event_loop()
    e = loop.run_until_complete(do_delay_release(sdk.release))
    print(e)


def test():
    # sdk = pyzenbo.connect(host)
    sdk.on_state_change_callback = on_state_change
    # sdk.on_result_callback = on_result
    # sdk.on_vision_callback = vision
    time.sleep(0.0001)
    # s = sdk.utility.follow_object(sync=True, timeout=10)
    s = sdk.motion.move_body(10, 0, 0, 2, timeout=3)
    # s = sdk.robot.speak('Hello World', {'speed': 50}, sync=True, timeout=10)
    # s = sdk.robot.set_expression(
    #     'PROUD',
    #     'I wander among the stars. Pass by the center of the galaxy',
    #     {'speed': 150}, sync=False)
    # s = sdk.utility.play_emotional_action('SHY', 22)
    # s = sdk.robot.speak(
    #     """
    #     I wander among the stars,
    #     Pass by the center of the galaxy,
    #     Travel between the normal space and planar space,
    #     and feel the every corner of space-time with space-sensory organ.
    #     I am an Abh, kin of the stars. Dear Stars,
    #     Please listen to the wishes of your short-lived kin.
    #     Our wishes, It is to live through the end of your senility.
    #     """
    # )
    # s = sdk.baidu.detect_face_from_photo(
    #     "content://com.android.providers.media.documents/document/image%3A25")
    # s = sdk.motion.move_head(0, 15, 1)
    # s = sdk.vision.request_detect_person()
    print('return:', s)
    delay_for_release(3)
    #
    # time.sleep(WHEEL_LIGHT_TEST_DELAY)
    # sdk.vision.request_detect_person()

    # sdk.robot.stop_speak(sync=False)
    # s = sdk.robot.speak('Hello World', sync=False)
    # print(s)


def speak_and_listen_test():
    domain = 'E7AABB554ACB414C9AB9BF45E7FA8AD9'
    sentence = 'Which city do you like? You can say Hello Block City, or Hello White City'
    s = sdk.robot.register_listen_callback(domain, listen)
    print('return:', s)
    s = sdk.robot.jump_to_plan(domain, 'lanuchHelloWolrd_Plan')
    print('return:', s)
    # s = sdk.robot.speak_and_listen(sentence)
    s = sdk.robot.wait_for_listen(sentence, timeout=20)
    time.sleep(0.1)
    print('wait_for_listen_return:', s)
    delay_for_release(1)


def line_follower_test():
    config = LineFollowerConfig()
    print(config.add_rule(0, 7, 2))
    print(config.build())
    print(sdk.lineFollower.follow_line(config.build(), sync=False))
    print(config.add_rule(4, 8, -90))
    print(sdk.lineFollower.update_config(1, config.build(), sync=False))
    delay_for_release(10)


def wait_for_test():
    s = sdk.vision.wait_for_detect_face(enable_debug_preview=True, timeout=10)
    print('wait_for_detect_face_return:', s)
    s = sdk.sensor.wait_for_trigger_key_event(10)
    print('wait_for_trigger_key_return:', s)
    s = sdk.sensor.wait_for_capacity_touch_sensor_event(0, 10)
    print('wait_for_capacity_touch_sensor_return:', s)
    s = sdk.vision.wait_for_recognize_person(user_id='aaa', enable_debug_preview=True, timeout=10)
    print('wait_for_recognize_person_return:', s)
    # time.sleep(5)
    delay_for_release(1)


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""
    result_template = {
        'success': {'state': 5, 'error': 0},
        'reject': {'state': 2, 'error': 197633},
        'fail': {'state': 4, 'error': 100663297},
    }

    # def setUp(self):
    #     print('setUP', threading.get_ident())
    #     sdk = PyZenboSDK((host, port))
    #     # sdk.on_state_change_callback = on_state_change
    #     # sdk.on_result_callback = on_result
    #     time.sleep(0.001)
    #
    # def tearDown(self):
    #     print('tearDown:', os.getpid())
    #     sdk.release()
    #     sdk = None
    #     time.sleep(1)

    def test_speak(self):
        print('test_speak')
        self.assertDictEqual(
            sdk.robot.speak('Hello World', {'speed': 50}, sync=True, timeout=10)[1],
            self.result_template['success'])

    def test_set_expression(self):
        print('test_set_expression')
        self.assertDictEqual(
            sdk.robot.set_expression(
                'ACTIVE',
                'I wander among the stars. Pass by the center of the galaxy')[1],
            self.result_template['success'])

    def test_query_expression(self):
        print('test_query_expression')
        self.assertDictEqual(
            sdk.robot.query_expression_status()[1],
            self.result_template['success'])

    def test_stop_speak(self):
        print('test_stop_speak')
        self.assertDictEqual(
            self._stop_speak(),
            self.result_template['success'])

    @staticmethod
    def _stop_speak():
        sdk.robot.speak('A long time ago in a galaxy far, far away....',
                        config={'speed': 75, 'pitch': 150, }, sync=False)
        time.sleep(1.5)
        return sdk.robot.stop_speak()[1]

    def test_move_body(self):
        print('test_move_body')
        self.assertDictEqual(
            sdk.motion.move_body(0.5, 1.5, 25, 2)[1],
            self.result_template['success'])

    def test_remote_move_body(self):
        print('test_remote_move_body')
        self.assertTupleEqual(
            self._remote_move_body(),
            (self.result_template['success'], self.result_template['success'])
        )

    def test_remote_move_head(self):
        print('test_remote_move_head')
        self.assertTupleEqual(
            self._remote_move_head(),
            (self.result_template['success'], self.result_template['success'])
        )

    @staticmethod
    def _remote_move_body():
        ret = sdk.motion.remote_control_body(2)[1]
        time.sleep(3)
        return ret, sdk.motion.stop_moving()[1]

    @staticmethod
    def _remote_move_head():
        ret = sdk.motion.remote_control_head(1)[1]
        time.sleep(1)
        return ret, sdk.motion.remote_control_head(0)[1]

    def test_move_head(self):
        print('test_head')
        self.assertDictEqual(
            sdk.motion.move_head(0, 30, 2)[1],
            self.result_template['success'])

    def test_wheel_light_color(self):
        print('test_wheel_light_color')
        self.assertDictEqual(
            sdk.wheelLight.set_color(0, 0xff, 0x00ED0517)[1],
            self.result_template['success'])

    def test_wheel_light_static(self):
        print('test_wheel_light_static')
        self.assertDictEqual(
            sdk.wheelLight.start_static(0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_strobing(self):
        print('test_wheel_light_start_strobing')
        self.assertDictEqual(
            sdk.wheelLight.start_strobing(0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_breath(self):
        print('test_wheel_light_start_breath')
        self.assertDictEqual(
            sdk.wheelLight.start_breath(0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_color_cycle(self):
        print('test_wheel_light_start_color_cycle')
        self.assertDictEqual(
            sdk.wheelLight.start_color_cycle(0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_rainbow(self):
        print('test_wheel_light_start_rainbow')
        self.assertDictEqual(
            sdk.wheelLight.start_rainbow(0, 0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_breath_rainbow(self):
        print('test_wheel_light_start_breath_rainbow')
        self.assertDictEqual(
            sdk.wheelLight.start_breath_rainbow(0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_comet(self):
        print('test_wheel_light_start_comet')
        self.assertDictEqual(
            sdk.wheelLight.start_comet(0, 0, 0)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_rainbow_comet(self):
        print('test_wheel_light_start_rainbow_comet')
        self.assertDictEqual(
            sdk.wheelLight.start_rainbow_comet(0, 1, -1)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_moving_flash(self):
        print('test_wheel_light_start_moving_flash')
        self.assertDictEqual(
            sdk.wheelLight.start_moving_flash(0, 1, -1)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_flash_dash(self):
        print('test_wheel_light_start_flash_dash')
        self.assertDictEqual(
            sdk.wheelLight.start_flash_dash(0, 1, -1)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_rainbow_wave(self):
        print('test_wheel_light_start_rainbow_wave')
        self.assertDictEqual(
            sdk.wheelLight.start_rainbow_wave(0, 1, 1)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_glowing_yoyo(self):
        print('test_wheel_light_start_glowing_yoyo')
        self.assertDictEqual(
            sdk.wheelLight.start_glowing_yoyo(0, 2)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_starry_night(self):
        print('test_wheel_light_start_starry_night')
        self.assertDictEqual(
            sdk.wheelLight.start_starry_night(1, -1, -1)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_start_wave(self):
        print('test_wheel_light_start_wave')
        self.assertDictEqual(
            sdk.wheelLight.start_wave(0, 2)[1],
            self.result_template['success'])
        time.sleep(WHEEL_LIGHT_TEST_DELAY)

    def test_wheel_light_turn_off(self):
        print('test_wheel_light_turn_off')
        self.assertDictEqual(
            sdk.wheelLight.turn_off(0)[1],
            self.result_template['success'])

    def test_utility_trace_face(self):
        print('test_utility_trace_face')
        self.assertGreater(sdk.utility.track_face(True, False)[0], 0)
        time.sleep(UTILITY_TEST_DELAY)
        self.assertDictEqual(
            sdk.cancel_command(zenbo_command.UTILITY_TRACK_FACE)[1],
            self.result_template['success']
        )

    def test_utility_follow_face(self):
        print('test_utility_follow_face')
        self.assertGreater(sdk.utility.follow_face(True, False)[0], 0)
        time.sleep(UTILITY_TEST_DELAY)
        self.assertDictEqual(
            sdk.cancel_command(zenbo_command.UTILITY_TRACK_FACE)[1],
            self.result_template['success']
        )

    def test_utility_follow_object(self):
        print('test_utility_trace_face')
        self.assertGreater(sdk.utility.follow_object()[0], 0)
        time.sleep(UTILITY_TEST_DELAY)
        self.assertDictEqual(
            sdk.cancel_command(zenbo_command.UTILITY_FOLLOW_OBJECT)[1],
            self.result_template['success']
        )


if __name__ == '__main__':
    # test()
    # speak_and_listen_test()
    # wait_for_test()
    unittest.main()
    print('unittest completed')
    sdk.release()
