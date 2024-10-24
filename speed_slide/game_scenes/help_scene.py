from tui import Scene, ForegroundColours, RichFormatText
from tui.controls import DialogueWindow, TxtLabel
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.io import safe_input


class HelpScene(Scene):
    """
    Display tutorial on how to play the game.
    """

    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, '!')
        [self.background_rft.set_format(i, slice(None), ForegroundColours.BLUE) for i in range(Constants.SCREEN_HEIGHT)]
        self.render()

    def play(self):
        """
        Displays the help information page-by-page.
        """
        page_counter: int = 0
        total_pages: int = 1
        while page_counter < total_pages:
            page_counter += 1
            self.show_dialogue(HelpScene.__get_page(page_counter), None)
            option = safe_input(
                RichFormatText(f'(Page {page_counter}/{total_pages}) Press enter for next page, or q to return to menu.')
                 .set_format(0, slice(None), ForegroundColours.BLUE)
            )
            if option == 'q':
                return

    @classmethod
    def __get_page(cls, page_num: int) -> DialogueWindow:
        """
        Construct the first page DialogueWindow and returns it.
        :param page_num: The page number.
        """
        dw = None
        dw_width = Constants.SCREEN_WIDTH - 6
        dw_height = Constants.SCREEN_HEIGHT - 4
        dw_x = 3
        dw_y = 2
        match page_num:
            case 1:
                dw = DialogueWindow('dw_p1', dw_width, dw_height, dw_x, dw_y,0,'',
                                    border_colour=ForegroundColours.CYAN)
                accumulated_y = 2
                lbl_para1 = TxtLabel('lbl_para1', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="The game starts with a game board of difficulty 1, which is a 3x3 grid. "
                                          "The grid is filled with numbers from 1 to 8, and one empty block at the "
                                          "bottom right corner. The board is then shuffled:")
                accumulated_y += lbl_para1.height + 1

                lbl_para2 = TxtLabel('lbl_para2', 42, 1, 31, accumulated_y, 0, auto_size=True,
                                     text="""
┌────┐┌────┐┌────┐     ┌────┐┌────┐┌────┐
│ 01 ││ 02 ││ 03 │     │ 05 ││ 01 ││ 02 │
└────┘└────┘└────┘     └────┘└────┘└────┘
┌────┐┌────┐┌────┐     ┌────┐┌────┐┌────┐
│ 04 ││ 05 ││ 06 │ ==> │ 04 ││ 06 ││ 03 │
└────┘└────┘└────┘     └────┘└────┘└────┘
┌────┐┌────┐┌────┐     ┌────┐┌────┐┌────┐
│ 07 ││ 08 ││    │     │ 07 ││    ││ 08 │
└────┘└────┘└────┘     └────┘└────┘└────┘
""")
                [lbl_para2.formatted_text.set_format(i, slice(None), ForegroundColours.MAGENTA) for i in range(1, 10)]
                accumulated_y += lbl_para2.height + 1

                lbl_para3 = TxtLabel('lbl_para3', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="Your main goal is to slide the blocks around to restore the numbers in their"
                                          " original order. During every move, you can only slide the block that is "
                                          "directly adjacent to the empty space, i.e. on top, bottom, left, or right of "
                                          "the empty space.")

                dw.controls.extend([lbl_para1, lbl_para2, lbl_para3])
        return dw
