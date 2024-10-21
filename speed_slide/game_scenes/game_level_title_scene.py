import time
from tui import Scene, ForegroundColours, TextFormats
from tui.controls import *
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.io import safe_input
from speed_slide.game_scenes.customised_controls import ScoreLabel


class GameLevelTitleScene(Scene):
    """
    The scene for displaying the title of a game level.
    """

    def __init__(self, level_difficulty: int, level_attempt: int, total_score: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

        self.__level_difficulty = level_difficulty
        self.__display_level_difficulty = level_difficulty - 2
        self.__level_attempt = level_attempt
        self.__total_score = total_score

    def play(self):
        # configure the dialogue box
        dw_level_title = DialogueWindow('dw_level_title', 30, 7,8, 0, 1, title='', border_colour=ForegroundColours.BLUE)

        # level title
        lbl_level = TxtLabel('lbl_level', 26, 1, 3, 2, 0,
                             text=f'Level  {self.__display_level_difficulty}-{self.__level_attempt}')
        (lbl_level.formatted_text
         .set_format(0, slice(0, 5), ForegroundColours.BLUE, text_format=TextFormats.UNDERLINE_AND_BOLD) # string 'Level'
         .set_format(0, slice(5, None), ForegroundColours.BLUE)) # string 'difficulty-attempt'

        # current total score
        lbl_current_score = TxtLabel('lbl_current_score', 20, 1, 3, 4, text='Score')
        lbl_current_score.formatted_text.set_format(0, slice(0, 6), ForegroundColours.BLUE, text_format=TextFormats.UNDERLINE_AND_BOLD)
        lbl_score = ScoreLabel('lbl_score', 0, x=10, y=4)

        dw_level_title.controls.extend([lbl_level, lbl_current_score, lbl_score])

        # configure the car
        lbl_car = TxtLabel('lbl_car', 27, 3, 0, 0, 1, text=r"""            _________
D~~~~~~~~#_/____|____\___
         └─(*)───────(*)─┘""")
        [lbl_car.formatted_text.set_format(i, slice(9 if i == 2 else 10, None), ForegroundColours.RED) for i in range(0, 3)] # the car
        (lbl_car.formatted_text
         .set_format(1, slice(0, 10), ForegroundColours.MAGENTA)) # the "road"

        # configure the road
        lbl_road = TxtLabel('lbl_road', 110, 5, 0, 14,
                            text='=' * 110 + '\n' + ' ' * 110 + '\n' + '  -  ' * 22 + '\n' + ' ' * 110 + '\n' + '=' * 110)
        (lbl_road.formatted_text
         .set_format(0, slice(0, 110), ForegroundColours.YELLOW)
         .set_format(4, slice(0, 110), ForegroundColours.YELLOW))

        self.add_control_at(lbl_road, 0, 15)
        self.add_control_at(dw_level_title, -lbl_car.width - dw_level_title.width, 12)
        self.add_control_at(lbl_car, -lbl_car.width, 16)

        # car tolls the level title from left to right
        for x in range(-lbl_car.width - dw_level_title.width, Constants.SCREEN_WIDTH + 6, 6):
            dw_level_title.x_coord = x
            lbl_car.x_coord = x + dw_level_title.width
            self.render()
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

            if x == 27: # at centre of the screen
                lbl_score.animate_change_score(self.__total_score, self.__total_score // 1919, self.on_scene_update, self)
                time.sleep(3)

        return lbl_road # this control is reused in the next scene