import time
from tui.controls import Control, TxtLabel
from tui import ForegroundColours, TextFormats
from speed_slide.__game_consts import _Constants as Constants


class ScoreLabel(Control):
    """
    A label for displaying scores up to 10 digits of positive scores and 9 digits of negative scores.
    """

    def __init__(self,
                 control_id: str,
                 score: int,
                 inactive_digit_colour: ForegroundColours = ForegroundColours.WHITE,
                 active_digit_colour: ForegroundColours = ForegroundColours.GREEN,
                 x: int = 0,
                 y: int = 0):
        super().__init__(control_id, 10, 1, x, y)

        self.inactive_digit_colour = inactive_digit_colour
        self.active_digit_colour = active_digit_colour

        self.__score = score
        self.__internal_txt_label: TxtLabel = TxtLabel(f'{control_id}__internal_txt_label', 10, 1, 0, 0, 0, text='0' * 10)
        self.__render()

    def animate_change_score(self, new_score: int, step: int = 0, screen_painter: callable = None):
        """
        Animates the change to a new score by step. If step is 0, the change is immediate.
        :param new_score: Target score.
        :param step: Step to change the score by.
        :param screen_painter: The function that is called to update the screen.
        """
        if self.__score == new_score:
            return

        if step == 0:
            self.__score = new_score
            self.__render()
            screen_painter() if screen_painter is not None else None
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)
            return

        for i in range(self.__score, new_score, step if new_score > self.__score else -step):
            self.__score = i if i + step <= new_score else new_score
            self.__render()
            screen_painter() if screen_painter is not None else None
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

    def render(self):
        """
        The rendering method can only be called internally.
        """
        pass

    def __render(self):
        """
        Internal renderer.
        """
        # changes score
        if self.__score >= 0:
            self.__internal_txt_label.text = f'{self.__score:0>10}'
        else:
            self.__internal_txt_label.text = f'-{-self.__score:0>9}'

        # changes colour
        (self.__internal_txt_label.formatted_text
         .set_format(0, slice(0, 11), self.inactive_digit_colour)
         .set_format(0, slice(10 - len(str(self.__score)), 11), self.active_digit_colour, text_format=TextFormats.BOLD))

        self.__internal_txt_label.render()
        self._internal_rft = self.__internal_txt_label.get_rft_object()