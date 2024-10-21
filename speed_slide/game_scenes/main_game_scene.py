from tui import Scene, ForegroundColours, RichFormatText, TextFormats
from tui.controls import TxtLabel, DialogueWindow
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.__debug import DebugTools
import random


class MainGameScene(Scene):
    """
    The main game scene.
    """

    def __init__(self, difficulty: int, attempt: int, total_score: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

        self.__difficulty = difficulty
        self.__attempt = attempt
        self.__total_score = total_score

        self.__gb = self.__GameBoard(difficulty)

        # main dialogue window
        dw_main = DialogueWindow('dw_main', Constants.SCREEN_WIDTH - 4, Constants.SCREEN_HEIGHT - 4, 2, 2,
                                 title='', border_colour=ForegroundColours.YELLOW)
        self.show_dialogue(dw_main, None)

        self.__target_moves = random.randint(20, 50)
        self.__debug_solution: list[int] = []
        self.__board_labels: dict[tuple[int, int], TxtLabel] = {}

        self.render()

    def play(self):
        """
        Starts the game
        """
        dw_main = self.get_control('dw_main') # type: DialogueWindow

        # ui setup

        # header label
        lbl_header = TxtLabel('lbl_header', 30, 1, 2, 3,
                              text='Solve the Slide Puzzle, FAST!')
        lbl_header.formatted_text.set_format(0, slice(30), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
        dw_main.controls.append(lbl_header)

        # generate labels from board
        self.__update_labels()

        # divider bar
        lbl_divider = TxtLabel('lbl_divider', 1, dw_main.height - 2, dw_main.width - 2 - 25, 1,
                               text='│\n' * (dw_main.height - 2))
        [lbl_divider.formatted_text.set_format(i, slice(0, 1), ForegroundColours.YELLOW, text_format=TextFormats.BOLD)
         for i in range(lbl_divider.height)]
        dw_main.controls.append(lbl_divider)

        self.render()

        # shuffle the game board
        for _ in range(self.__target_moves):
            while True:
                move = random.choice(self.__gb.adjacent)
                if len(self.__debug_solution) == 0 or move != self.__debug_solution[0]:
                    break
            self.__gb.slide(move)
            self.__debug_solution.insert(0, move)

    def __update_labels(self):
        """
        Create labels representing the game board.
        """
        # create labels if there isn't any
        if len(self.__board_labels) == 0:
            for item in self.__gb.board:
                x_start = (self.get_control('dw_main').width - 4 - self.__difficulty * 6 - 25 - 1) // 2 + 2 # exclude divider
                y_start = (self.get_control('dw_main').height - 4 - self.__difficulty * 3) // 2 + 2
                x, y = item
                label = TxtLabel(f'lbl_block:{x};{y}', 6, 3, x_start + x * 6, y_start + y * 3,
                                 text=f'{self.__gb.board[item]:0>2}', draw_borders=True,
                                 border_colour=ForegroundColours.MAGENTA,
                                 padding_top=1, padding_bottom=1, padding_left=2, padding_right=2)
                label.formatted_text.set_format(0, slice(2), label.border_colour)
                if label.text == '00':
                    label.text = '  '
                self.__board_labels[item] = label
            self.get_control('dw_main').controls.extend(list(self.__board_labels.values()))
            return

        # update existing
        for (x, y), num in self.__gb.board:
            lbl = self.__board_labels[(x, y)]
            lbl.text = f'{num:0>2}' if num != 0 else '  '
        self.render()

    class __GameBoard:
        """
        An internal class for dealing with the game board.
        """

        def __init__(self, difficulty: int):
            self.__difficulty = difficulty

            self.board: dict[tuple[int, int], int] = {}
            counter = 1
            for y in range(difficulty):
                for x in range(difficulty):
                    self.board[(x, y)] = counter
                    counter += 1
            # set last block to 0
            self.board[(difficulty - 1, difficulty - 1)] = 0

            self.adjacent: list[int] = []
            self.__empty_index = (difficulty - 1, difficulty - 1)
            self.find_adjacent()
            self.solved = False

        def slide(self, number: int) -> bool:
            """
            Slides the block with the specified number.
            :return: Returns whether the slide is valid. ValueError is raised if the number is not on the board.
            """
            if number not in self.board.values():
                raise ValueError(f'Number {number} is not on the board.')
            if number not in self.adjacent:
                return False

            number_index = list(self.board.keys())[list(self.board.values()).index(number)]
            # swap
            self.board[number_index], self.board[self.__empty_index] = self.board[self.__empty_index], self.board[number_index]
            self.find_adjacent()
            return True

        def find_adjacent(self):
            """
            Finds the adjacent numbers of the empty block (0), and stores them in self.__adjacent.
            """
            self.adjacent.clear()
            self.__empty_index = list(self.board.keys())[list(self.board.values()).index(0)]
            empty_x, empty_y = self.__empty_index
            adjacent_indices = (
                (empty_x - 1, empty_y), # left
                (empty_x + 1, empty_y), # right
                (empty_x, empty_y - 1), # up
                (empty_x, empty_y + 1), # down
            )
            for index in adjacent_indices:
                value = self.board.get(index, None)
                if value is None:
                    continue
                self.adjacent.append(value)

        def check_if_solved(self):
            """
            Checks if the board has been solved. Result is stored in self.solved.
            """
            solved = False
            counter = 1
            for y in range(self.__difficulty):
                for x in range(self.__difficulty):
                    solved = self.board[(x, y)] == (counter if x != self.__difficulty - 1 and y != self.__difficulty - 1 else 0)
                    counter += 1
            self.solved = solved
