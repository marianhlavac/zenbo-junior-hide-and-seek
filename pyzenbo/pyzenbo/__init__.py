from .modules import error_code
from .modules import zenbo_command
from .modules.inter_communication import STATE
from .modules.line_follower import LineFollowerConfig
from .py_zenbo_sdk import PyZenbo

__version__ = '1.0.7.1924'


def connect(destination, on_state_change_callback=None,
            on_result_callback=None):
    return PyZenbo(destination, on_state_change_callback, on_result_callback)
