import sys
import json
import pyzenbo
import time
from functools import partial
from hideandseek import dialog, navigation, seeking, comm

def main():
    """
    Robot main logic
    """
    if len(sys.argv) < 2:
        print('usage: hideandseek <robot_ip_address>')
        sys.exit(1)

    # Connect to the robot
    zenbo = comm.connect_robot(sys.argv[1])

    # Initialize
    listen_callback_handler = partial(dialog.handle_speak, zenbo)
    zenbo.robot.register_listen_callback(1207, listen_callback_handler)

    # Ask user if he wants to play
    dialog.say_fine(zenbo)
    # dialog.ask_user_for_play(zenbo)

    # Wait for response
    # TBD

    # Detect person who wants to play
    # TBD
    # seeking.detect_person()

    # Countdown
    # TBD
    # dialog.start_countdown()

    # Seek for the previously saved person
    # TBD
    # seeking.start_seeking()

    # ...

    # zenbo.motion.move_body(0.15, speed_level=2)
    # zenbo.motion.move_head(pitch_degree=-10)
    # zenbo.motion.move_head(pitch_degree=-10)
    # zenbo.motion.move_body(0.15, speed_level=2)
    # zenbo.cancel_command_by_serial(?)
    # zenbo.robot.speak_and_listen("")

    zenbo.release()
    sys.exit(0)

if __name__ == '__main__':
    main()