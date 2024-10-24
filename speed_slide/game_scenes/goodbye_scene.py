from tui import Scene, ForegroundColours
from tui.controls import TxtLabel
from speed_slide.__game_consts import _Constants as Constants
import time


class GoodbyeScene(Scene):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

        lbl_bye = TxtLabel('lbl_bye', 76, 12, 17, 9, 0,
"""
   █████████                        █████ █████                         ░███
  ███░░░░░███                      ░░███ ░░███                          ░███
 ███     ░░░   ██████   ██████   ███████  ░███████  █████ ████  ██████  ░███
░███          ███░░███ ███░░███ ███░░███  ░███░░███░░███ ░███  ███░░███ ░███
░███    █████░███ ░███░███ ░███░███ ░███  ░███ ░███ ░███ ░███ ░███████  ░███
░░███  ░░███ ░███ ░███░███ ░███░███ ░███  ░███ ░███ ░███ ░███ ░███░░░   ░░░ 
 ░░█████████ ░░██████ ░░██████ ░░████████ ████████  ░░███████ ░░██████   ███
  ░░░░░░░░░   ░░░░░░   ░░░░░░   ░░░░░░░░ ░░░░░░░░    ░░░░░███  ░░░░░░   ░░░ 
                                                     ███ ░███              
                                                    ░░██████               
                                                     ░░░░░░                """)
        [lbl_bye.formatted_text.set_format(i, slice(None), ForegroundColours.BLUE) for i in range(12)]
        self.add_control_at(lbl_bye, lbl_bye.x_coord, lbl_bye.y_coord)

    def play(self):
        time.sleep(3)
