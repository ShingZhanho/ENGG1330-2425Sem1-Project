from speed_slide.io import safe_input
from tui import Scene, ForegroundColours, TextFormats, RichFormatText
from tui.controls import DialogueWindow, TxtLabel
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.game_scenes.customised_controls import ScoreLabel
import time


class LevelSummaryScene(Scene):
    """
    Displaying the summary (scores, awards, statistics, etc.) of the previous game level.
    """

    def __init__(self, total_score: int, awards: tuple[str, int], level_up: bool, is_top: bool):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
        self.total_score = total_score
        self.awards = awards
        self.level_up = level_up
        self.is_top = is_top

    def play(self) -> int:
        """
        Play the scene. Returns the new total score.
        :return: New total score.
        """
        dw = DialogueWindow('dw', 82, 22, 14, 4, 0, 'LEVEL  CLEARED',
                            border_colour=ForegroundColours.YELLOW)

        lbl_congrats = TxtLabel('lbl_congrats', 40, 1, 20, 2, 0,
                                'CONGRATULATIONS! Let\'s see how you did!')
        lbl_congrats.formatted_text.set_random_colours_to_all(except_foreground=[ForegroundColours.BLACK, ForegroundColours.WHITE])

        lbl_event_name = TxtLabel('lbl_event_name', 30, 3, 11, 4, 0, '',
                                  padding_left=2, padding_right=2, padding_top=1, padding_bottom=1, draw_borders=True,
                                  border_colour=ForegroundColours.RED)
        lbl_event_score = TxtLabel('lbl_event_score', 30, 3, 41, 4, 0, '',
                                   padding_left=2, padding_right=2, padding_top=1, padding_bottom=1, draw_borders=True,
                                   border_colour=ForegroundColours.MAGENTA)

        lbl_score_from_level = TxtLabel('lbl_score_from_level', 30, 1, 21, 8, 0, 'Points earned from this level:')
        lbl_score_from_level.formatted_text.set_format(0, slice(None), ForegroundColours.BLUE, text_format=TextFormats.BOLD)

        score_lbl_level = ScoreLabel('score_lbl_level', 0, x=55, y=8)

        lbl_total_score = TxtLabel('lbl_total_score', 30, 1, 21, 9, 0, 'Total score:')
        lbl_total_score.formatted_text.set_format(0, slice(None), ForegroundColours.BLUE, text_format=TextFormats.BOLD)

        score_lbl_total = ScoreLabel('score_lbl_total', self.total_score, x=55, y=9)

        dw.controls.extend([
            lbl_congrats,
            lbl_event_name,
            lbl_event_score,
            lbl_score_from_level,
            score_lbl_level,
            lbl_total_score,
            score_lbl_total
        ])

        self.show_dialogue(dw, None)
        time.sleep(1)

        total_score_change = 0

        for name, score_change in self.awards:
            lbl_event_name.text = f'{name: ^26}'
            lbl_event_score.text = f'{score_change: ^26}'
            (lbl_event_score.formatted_text
             .set_format(0, slice(None), ForegroundColours.GREEN if score_change >= 0 else ForegroundColours.RED))

            self.render()
            time.sleep(0.6)

            total_score_change += score_change
            step = int(0.1919191919 * 10 ** (len(str(abs(score_change))) - 1))
            score_lbl_level.animate_change_score(total_score_change, step, self.on_scene_update, self)

            time.sleep(1)

            lbl_event_name.text = ''
            lbl_event_score.text = ''
            self.render()
            time.sleep(0.6)

        self.total_score = min(self.total_score + total_score_change, 9999999999)
        step = int(0.1919191919 * 10 ** (len(str(self.total_score)) - 1))
        score_lbl_total.animate_change_score(self.total_score, step, self.on_scene_update, self)

        result_text = ('Promoted to the next level!! Challenge yourself!' if self.level_up else
                       'Let\'s stay at this level and practice more!')
        text_colour = ForegroundColours.GREEN if self.level_up else ForegroundColours.RED

        if self.is_top:
            result_text = 'MASTER OF SLIDE! You are at the top level! Continue to challenge yourself!'
            text_colour = ForegroundColours.YELLOW

        lbl_result = TxtLabel('lbl_result', len(result_text), 1, (80 - len(result_text)) // 2, 18, 0, result_text)
        lbl_result.formatted_text.set_format(0, slice(None), text_colour, text_format=TextFormats.BOLD)

        dw.controls.append(lbl_result)
        self.render()

        safe_input(RichFormatText('Press Enter to continue...'))

        return self.total_score