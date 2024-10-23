from tui import Scene, ForegroundColours, TextFormats
from tui.controls import TxtLabel
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.game_scenes.customised_controls import ScoreLabel
import time


class GameOverScene(Scene):
    """
    Displayed when the user loses the game.
    """

    def __init__(self, final_score: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        self.final_score = final_score

        lbl_road_and_car = TxtLabel('lbl_road_and_car', 110, 8, 0, 12, 0,
                                    """ 
                                    ┌─   ───────(*)─┐
                                    ¯¯¯\¯¯¯¯|¯¯¯¯/      (*)
========================================¯¯¯¯¯¯¯¯¯=============================================================

  -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -    -  
  
==============================================================================================================""")
        [lbl_road_and_car.formatted_text.set_format(i, slice(None), ForegroundColours.YELLOW) for i in range(3, 8)]

        # car colour
        (lbl_road_and_car.formatted_text
         .set_format(1, slice(36, 53), ForegroundColours.RED)
         .set_format(2, slice(36, 59), ForegroundColours.RED)
         .set_format(3, slice(40, 49), ForegroundColours.RED))

        self.add_control_at(lbl_road_and_car, lbl_road_and_car.x_coord, lbl_road_and_car.y_coord)

        self.render()

    def play(self):
        lbl_game_over = TxtLabel('lbl_game_over', 78, 6, 16, -5, 0, text=
                                 """ ██████╗  █████╗ ███╗   ███╗███████╗      ██████╗ ██╗   ██╗███████╗██████╗ ██╗
██╔════╝ ██╔══██╗████╗ ████║██╔════╝     ██╔═══██╗██║   ██║██╔════╝██╔══██╗██║
██║  ███╗███████║██╔████╔██║█████╗       ██║   ██║██║   ██║█████╗  ██████╔╝██║
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝       ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚═╝
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗     ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║██╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝""")

        [lbl_game_over.formatted_text.set_format(i, slice(None), ForegroundColours.RED) for i in range(6)]
        self.controls.append(lbl_game_over)

        for y in range(-5, 4):
            lbl_game_over.y_coord = y
            self.render()
            time.sleep(0.1)

        lbl_final_score = TxtLabel('lbl_final_score', 42, 4, 34, 22, 0, text=f'{"FINAL SCORE": ^40}',
                                   padding_left=1, padding_right=1, padding_top=1, padding_bottom=2, draw_borders=True,
                                   border_colour=ForegroundColours.BLUE)
        self.controls.append(lbl_final_score)
        self.render()
        time.sleep(1)

        score_label = ScoreLabel('score_lbl', 0, x=50, y=24)
        self.controls.append(score_label)
        self.render()
        step = int(0.1919191919 * 10 ** (len(str(self.final_score)) - 1))
        score_label.animate_change_score(self.final_score, step, self.on_scene_update, self)

        lbl_continue = TxtLabel('lbl_continue', 32, 1, 39, 27, text='Press enter to return to menu...')
        lbl_continue.formatted_text.set_format(0, slice(None), ForegroundColours.YELLOW, text_format=TextFormats.BOLD)

        time.sleep(1)
        self.controls.append(lbl_continue)
        self.render()

        input()