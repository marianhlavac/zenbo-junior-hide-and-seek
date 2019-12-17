import json

import pyzenbo
import pyzenbo.modules.zenbo_command as commands
import time


# some stupid code generte by: https://zenbolab.asus.com/?lang=en

def main():
    """
    Stupid main method that shows how we maybe code the robot
    :return:
    """
    zenbo = pyzenbo.connect('')  # TODO insert ip here
    serialNumber = ""  # TODO insert serial nr here

    def listen_callback(args):
        event_user_utterance = args.get('event_user_utterance', None)
        if event_user_utterance and 'move forward' == str(
                json.loads(event_user_utterance.get('user_utterance'))[0].get('result')[0]):
            zenbo.motion.move_body(0.15, speed_level=2)

    zenbo.robot.register_listen_callback(1207, listen_callback)

    zenbo.motion.move_body(0.15, speed_level=2)
    zenbo.motion.move_head(pitch_degree=-10)
    zenbo.motion.move_head(pitch_degree=-10)
    zenbo.motion.move_body(0.15, speed_level=2)
    zenbo.cancel_command_by_serial(serialNumber)
    zenbo.speak_and_listen("")

    zenbo.release()


if __name__ == '__main__':
    main()
