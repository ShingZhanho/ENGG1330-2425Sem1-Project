from tui import Scene, ForegroundColours, RichFormatText, TextFormats
from tui.controls import DialogueWindow, TxtLabel
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.io import safe_input, beep


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
        page_counter: int = 1
        total_pages: int = 5 # UPDATE THIS VALUE WHEN ADDING MORE PAGES
        while page_counter <= total_pages:
            self.show_dialogue(HelpScene.__get_page(page_counter), None)
            option = safe_input(
                RichFormatText(f'(Page {page_counter}/{total_pages}) Commands: [N] - Next page; [P] - '
                               f'Previous page; [Q] - Returns to main menu\n')
                 .set_format(0, slice(None), ForegroundColours.MAGENTA)
            ).lower()
            if option == 'q':
                return
            elif option == 'p':
                if page_counter == -1:
                    beep()
                else:
                    page_counter -= 1
            elif option == 'n':
                if page_counter == total_pages:
                    beep()
                else:
                    page_counter += 1
            else:
                beep()

    @classmethod
    def __get_page(cls, page_num: int) -> DialogueWindow:
        """
        Construct the first page DialogueWindow and returns it.
        :param page_num: The page number.
        """
        dw_width = Constants.SCREEN_WIDTH - 6
        dw_height = Constants.SCREEN_HEIGHT - 4
        dw_x = 3
        dw_y = 2
        dw = DialogueWindow('dw_name_pending', dw_width, dw_height, dw_x, dw_y, 0, 'HELP',
                            border_colour=ForegroundColours.CYAN)
        accumulated_y = 2 # calculating the y-coordinate of the controls
        match page_num:
            # ================================= START [PAGE -1] ==============================
            case -1:
                dw.controls_id='dw_hidden_page'

                lbl_para1 = TxtLabel('lbl_para1', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                        text="YOU GOTTA BE JOKING! Why would you want to go page -1?!\n\n\n"
                                             "Anyway, here's a hidden trick for you:\n\n"
                                             "Type \'/give-up?\' at the start of a level will give you the solution. "
                                             "REMEMBER! The solution only works when the board has not been touched.")

                dw.controls.append(lbl_para1)
            # ================================= START [PAGE 1] ===============================
            case 1:
                dw.control_id = 'dw_page1'

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
                                          " original order. In each move, you can only slide the block that is "
                                          "directly adjacent to the empty space, i.e. on top, bottom, left, or right of "
                                          "the empty space.\n\n"
                                          "To make a move, enter the number of the block you want to slide into the "
                                          "the empty space, then press enter. "
                                          "If you want to leave the game immediately, type the command \'/quit\' and "
                                          "press enter. If you simply want to give up and see your final score, you "
                                          "can use the command \'/surrender\'.")

                dw.controls.extend([lbl_para1, lbl_para2, lbl_para3])
            # ================================= END [PAGE 1] =================================

            # ================================= START [PAGE 2] ===============================
            case 2:
                dw.control_id = 'dw_page2'

                lbl_para1 = TxtLabel('lbl_para1', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="On the right hand side of the screen, you will see three numbers:\n\n"
                                          "  - Target moves: Your target of moves to solve the puzzle.\n"
                                          "  - Max. moves: The maximum number of moves allowed in the level.\n"
                                          "  - Moves: The number of moves you have made so far.")
                accumulated_y += lbl_para1.height + 2

                lbl_para2 = TxtLabel('lbl_para2', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="Try to make as few moves as possible to solve the puzzle!\n\n"
                                          "If you make moves less than or equal to the target moves, you will earn extra"
                                          " points and get promoted to the next difficulty level.\n\n"
                                          "If you solve the the puzzle within the maximum moves but exceed the target"
                                          " moves, you will still get basic points for solving the puzzle, but you will"
                                          " stay on the same difficulty level.\n\n"
                                          "If you cannot solve the puzzle within the maximum moves, the game ends "
                                          "immediately.")
                accumulated_y += lbl_para2.height + 2

                lbl_para3 = TxtLabel('lbl_para3', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="WATCH OUT! If you make moves more than the target moves, there will be some"
                                          " random events happening as the game goes on. They can either give you bonus"
                                          " scores or take away your points. A wicked witch is waiting to haunt you!")
                lbl_para3.formatted_text.set_format(0, slice(11), ForegroundColours.RED, text_format=TextFormats.BOLD)

                dw.controls.extend([lbl_para1, lbl_para2, lbl_para3])
            # ================================= END [PAGE 2] =================================

            # ================================= START [PAGE 3] ===============================
            case 3:
                dw.controls_id = 'dw_page3'

                lbl_para1 = TxtLabel('lbl_para1', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                     text="As the the difficulty level increases, the game board will become larger. "
                                          "It starts off as 3x3 and can get as large as 6x6. The more complex the board"
                                          "the more points you get when you solve it.\n\n"
                                          "Have fun and enjoy the game!")

                lbl_keep_reading = TxtLabel('lbl_keep_reading', dw_width - 4, 1, 2, 10, 0, auto_size=True,
                                            text="Keep reading for a general solution that works for every slide puzzle"
                                                 ", or return to the main menu and start a new game to discover your"
                                                 "own method of solving the puzzle.")
                accumulated_y = lbl_keep_reading.y_coord + lbl_keep_reading.height + 1

                lbl_spoiler = TxtLabel('lbl_spoiler', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                       text="SPOILER ALERT! The general solution applies to all sliding puzzles and "
                                            "may spoil the fun part - trying - of the game. Turn to the next page only "
                                            "if you are desperate to win. ;-)")
                [lbl_spoiler.formatted_text
                 .set_format(i, slice(None), ForegroundColours.RED, text_format=TextFormats.BOLD)
                 for i in range(lbl_spoiler.height)]

                dw.controls.extend([lbl_para1, lbl_keep_reading, lbl_spoiler])
            # ================================= END [PAGE 3] =================================

            # ================================= START [PAGE 4] ===============================
            case 4:
                dw.controls_id = 'dw_page4'

                lbl_step1_heading = TxtLabel('lbl_step1_heading', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                             text="STEP 1")
                lbl_step1_heading.formatted_text.set_format(0, slice(None), text_format=TextFormats.UNDERLINE)
                accumulated_y += lbl_step1_heading.height + 1

                lbl_step1 = TxtLabel('lbl_step1', dw_width - 8, 1, 6, accumulated_y, 0, auto_size=True,
                                     text="Solve the first horizontal row from left to right first, but leave the last"
                                          " two blocks for later. For example, if the board is 4x4, solve for numbers 1"
                                          " and 2 first, and leave numbers 3 and 4 alone for now.")
                accumulated_y += lbl_step1.height + 1

                lbl_step2_heading = TxtLabel('lbl_step2_heading', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                                text="STEP 2")
                lbl_step2_heading.formatted_text.set_format(0, slice(None), text_format=TextFormats.UNDERLINE)
                accumulated_y += lbl_step2_heading.height + 1

                lbl_step2 = TxtLabel('lbl_step2', dw_width - 8, 1, 6, accumulated_y, 0, auto_size=True,
                                     text="Move the second last block of the row to the last spot of the row. For "
                                          "example, if the first row is 01 02 ?? ?? now, move 03 to the last spot of"
                                          " the row, turning it into 01 02 ?? 03.\n\nThen, move the last block of the "
                                          "row directly below the last spot of the row. Keeping the above example, 04 "
                                          "should now be moved directly below 03.\n\nNow, you can slide 03 and 04 back "
                                          "into their original spots. The first row should now be solved.")
                accumulated_y += lbl_step2.height + 1

                lbl_step3_heading = TxtLabel('lbl_step3_heading', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                                text="STEP 3")
                lbl_step3_heading.formatted_text.set_format(0, slice(None), text_format=TextFormats.UNDERLINE)
                accumulated_y += lbl_step3_heading.height + 1

                lbl_step3 = TxtLabel('lbl_step3', dw_width - 8, 1, 6, accumulated_y, 0, auto_size=True,
                                     text="Now solve the first vertical column from top to bottom, but leave the last "
                                          "two blocks for later. For example, if the board is 4x4, the first column "
                                          "should be 01 05 ?? ??. Notice that 01 is already in place from STEP 1, so "
                                          "you only need to solve for 05.")

                lbl_tbc = TxtLabel('lbl_tbc', dw_width - 2, 1, 1, dw_height - 2, 0, auto_size=True,
                                   text=f"{'Go on to the next page >>': >{dw_width - 2}}")

                dw.controls.extend([lbl_step1_heading, lbl_step1, lbl_step2_heading, lbl_step2,
                                    lbl_step3_heading, lbl_step3, lbl_tbc])
            # ================================= END [PAGE 4] =================================

            # ================================= START [PAGE 5] ===============================
            case 5:
                dw.controls_id = 'dw_page5'

                lbl_step4_heading = TxtLabel('lbl_step4_heading', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                                text="STEP 4")
                lbl_step4_heading.formatted_text.set_format(0, slice(None), text_format=TextFormats.UNDERLINE)
                accumulated_y += lbl_step4_heading.height + 1

                lbl_step4 = TxtLabel('lbl_step4', dw_width - 8, 1, 6, accumulated_y, 0, auto_size=True,
                                     text="Now move the second last block of the column to the last spot of the column."
                                          " For example, if the first column is 01 05 ?? ?? now, move 09 to the last "
                                          "spot of the column, turning it into 01 05 ?? 09.\n\nThen, move the last "
                                          "block of the column directly to the right of the last spot of the column. "
                                          "Keeping the above example, 13 should now be moved directly to the right of "
                                          "09.\n\nNow, you can slide 09 and 13 back into their original spots. The "
                                          "first column should now be solved.")
                accumulated_y += lbl_step4.height + 1

                lbl_step5_heading = TxtLabel('lbl_step5_heading', dw_width - 4, 1, 2, accumulated_y, 0, auto_size=True,
                                                text="STEP 5")
                lbl_step5_heading.formatted_text.set_format(0, slice(None), text_format=TextFormats.UNDERLINE)
                accumulated_y += lbl_step5_heading.height + 1

                lbl_step5 = TxtLabel('lbl_step5', dw_width - 8, 1, 6, accumulated_y, 0, auto_size=True,
                                     text="Repeat STEP 1 to STEP 2 to solve the second horizontal row, and then repeat "
                                          "STEP 3 to STEP 4 to solve the second vertical column. Then solve the third "
                                          "row and column, and so on, until the board is solved.")

                dw.controls.extend([lbl_step4_heading, lbl_step4, lbl_step5_heading, lbl_step5])

        return dw
