"""
Voice recognition and dialog related functions to interact between Zenbo
and the user.
"""
import pyzenbo
import json

def handle_speak(zenbo: pyzenbo.PyZenbo, args):
    """
    Handles user speaking -- whenever user says something, Zenbo calls this function.
    """
    event_user_utterance = args.get('event_user_utterance', None)
    been_said = str(json.loads(event_user_utterance.get('user_utterance'))[0].get('result')[0])
    if event_user_utterance and been_said == 'move forward':
        zenbo.motion.move_body(0.15, speed_level=2)

def ask_user_for_play(zenbo: pyzenbo.PyZenbo):
    """
    Asks the user if he/she wants to play some hide and seek.
    """
    pass

def say_fine(zenbo: pyzenbo.PyZenbo):
    """
    FFFFINE.
    """
    zenbo.robot.speak('Fine.')