from speed_slide.__game_consts import _Constants as Constants
from tui import RichFormatText


class DebugTools:
    """
    Internal tools for debugging.
    """

    def __init__(self):
        self.__debug_msg = None

    @property
    def debug_msg(self):
        val = self.__debug_msg
        self.__debug_msg = None # msg is used only once
        return val

    @debug_msg.setter
    def debug_msg(self, value: RichFormatText):
        self.__debug_msg = value

    def write_to_log(self, caller: str, msg: str):
        if not Constants.DEBUG:
            return