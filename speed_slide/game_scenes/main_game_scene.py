from tui import Scene, ForegroundColours, RichFormatText, TextFormats, BackgroundColours
from tui.controls import TxtLabel, DialogueWindow
from tui import transitions
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.io import safe_input
from speed_slide.game_scenes.__random_events_ascii_arts import EventASCIIArts as ASCIIArts
import random
import time


class MainGameScene(Scene):
    """
    The main game scene.
    """

    def __init__(self, difficulty: int, attempt: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

        self.__difficulty = difficulty
        self.__attempt = attempt
        self.exit_transition = transitions.slide_from_right

        self.__gb = self.__GameBoard(difficulty)

        # main dialogue window
        dw_main = DialogueWindow('dw_main', Constants.SCREEN_WIDTH - 4, Constants.SCREEN_HEIGHT - 4, 2, 2,
                                 title='', border_colour=ForegroundColours.YELLOW)
        self.show_dialogue(dw_main, None)

        self.__target_moves = random.randint(difficulty ** 2, difficulty ** 3)
        self.__debug_solution: list[int] = []
        self.__board_labels: dict[tuple[int, int], TxtLabel] = {}

        self.render()

    def play(self):
        """
        Starts the game and returns the game result.
        Result is in the form of a tuple. The elements are:
        - [0] status: int = -1 for quit, 0 for win (advance to new difficulty), 1 for win (same difficulty), 2 for lose
        - [1] awards: list[tuple[str, int]] = awards/penalties given, in the form of (reason: str, score: int)
        """
        dw_main = self.get_control('dw_main') # type: DialogueWindow

        # ui setup

        # header label
        lbl_header = TxtLabel('lbl_header', 30, 1, 4, 2,
                              text='Solve the Slide Puzzle, FAST!')
        lbl_header.formatted_text.set_format(0, slice(30), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
        dw_main.controls.append(lbl_header)

        # footer label
        lbl_footer = TxtLabel('lbl_footer', 35, 2, 4, dw_main.height - 4,
                              text='You may slide the following blocks:\n  01 02 03 04')
        (lbl_footer.formatted_text
         .set_format(0, slice(35), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
         .set_format(1, slice(13), ForegroundColours.CYAN))

        # generate labels from board
        self.__update_labels()

        # divider bar
        lbl_divider = TxtLabel('lbl_divider', 1, dw_main.height - 2, dw_main.width - 2 - 25, 1,
                               text='│\n' * (dw_main.height - 2))
        [lbl_divider.formatted_text.set_format(i, slice(0, 1), ForegroundColours.YELLOW, text_format=TextFormats.BOLD)
         for i in range(lbl_divider.height)]
        dw_main.controls.append(lbl_divider)

        self.render()

        time.sleep(1)

        # blind blocks temporarily, row by row
        for y in range(self.__difficulty):
            for x in range(self.__difficulty):
                lbl = self.__board_labels[(x, y)]
                lbl.text = '??'
                self.render()
                time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

        # shuffle the game board
        last_n_moves = [] # stores last n moves to reduce redundant random moves, n = difficulty
        for _ in range(self.__target_moves if not Constants.DEBUG else 3):
            while True:
                move = random.choice(self.__gb.adjacent)
                if move not in last_n_moves or all(self.__gb.adjacent[i] in last_n_moves for i in range(len(self.__gb.adjacent))):
                    break
            self.__gb.slide(move)
            self.__debug_solution.insert(0, move)
            last_n_moves.append(move)
            if len(last_n_moves) > self.__difficulty:
                last_n_moves.pop(0)

        time.sleep(1)

        # reveal blocks, row by row
        for y in range(self.__difficulty):
            for x in range(self.__difficulty):
                lbl = self.__board_labels[(x, y)]
                lbl.text = f'{self.__gb.board[(x, y)]:0>2}' if self.__gb.board[(x, y)] != 0 else '  '
                self.render()
                time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

        dw_main.controls.append(lbl_footer)

        terminate_signal = False

        moves = 0
        self.__target_moves = int(self.__target_moves * 1.3)
        max_moves = int(self.__target_moves * 2.5)

        # right hand side info
        lbl_target = TxtLabel('lbl_target', 25, 2, dw_main.width - 25, 2,
                              text=f'TARGET MOVES\n  {self.__target_moves}')
        (lbl_target.formatted_text
             .set_format(0, slice(25), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
             .set_format(0, slice(25), ForegroundColours.MAGENTA))

        lbl_max = TxtLabel('lbl_max', 25, 2, dw_main.width - 25, 5,
                          text=f'MAX MOVES\n  {max_moves}')
        (lbl_max.formatted_text
            .set_format(0, slice(25), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
            .set_format(0, slice(25), ForegroundColours.MAGENTA))

        lbl_moves = TxtLabel('lbl_moves', 25, 2, dw_main.width - 25, 8,
                             text=f'MOVES\n  {moves}')
        (lbl_moves.formatted_text
            .set_format(0, slice(25), ForegroundColours.MAGENTA, text_format=TextFormats.UNDERLINE_AND_BOLD)
            .set_format(0, slice(25), ForegroundColours.MAGENTA))

        lbl_objectives = TxtLabel('lbl_objectives', 24, 14, dw_main.width - 25, 12,
                                  text="[OBJECTIVES]\n" 
                                       "Slide the blocks in order to solve the puzzle. Make as few moves as possible. "
                                       "Solve under the target moves to earn bonus points! Watch out, random events may"
                                       " happen when you are over the target moves and you lose when you exceed the "
                                       "max moves!", auto_size=True)

        dw_main.controls.extend([lbl_target, lbl_max, lbl_moves, lbl_objectives])

        # for random events:
        blind_event_counter = 0 # max = self.__difficulty - 2
        blinded_blocks: list[int] = []

        # main game loop
        while not self.__gb.solved:
            # update footer
            available_options = '  '
            for i in range(4):
                item = self.__gb.adjacent[i] if i < len(self.__gb.adjacent) else '--'
                available_options += f'{item:0>2} '
            lbl_footer.text = f'You may slide the following blocks:\n{available_options}'

            # update moves
            lbl_moves.text = f'MOVES\n  {moves}'
            self.render()

            awards: list[tuple[str, int]] = [] # refer to docstring for awards/penalties

            # get user input
            while not terminate_signal and not moves >= max_moves:
                user_input = safe_input(RichFormatText('Enter the block number to slide: ')
                                        .set_format(0, slice(33), ForegroundColours.WHITE, background=ForegroundColours.MAGENTA))
                # validate input
                # match input with commands
                match user_input.lower():
                    case '/quit':
                        terminate_signal = True
                        break
                    case '/give-up?':
                        lbl_solution = TxtLabel('lbl_solution', 110, 1, 0, 0, auto_size=True,
                                                text='Never gonna give you up! ANS: ' + ' '.join(str(x) for x in self.__debug_solution))
                        self.add_control_at(lbl_solution, 0, 0)
                        break
                if not str.isnumeric(user_input):
                    self.__display_error('Invalid input! Please enter a number from the available options.')
                    continue
                user_input = int(user_input)
                if not 1 <= user_input <= self.__difficulty ** 2 - 1:
                    self.__display_error('Invalid input! That block doesn\'t exist! Are you having illusions!?')
                    continue
                if user_input not in self.__gb.adjacent:
                    self.__display_error('Invalid input! You cannot slide this block to the empty space directly!')
                    continue
                moves += 1
                self.__gb.slide(user_input)
                break

            if terminate_signal:
                return -1, None
            if moves >= max_moves:
                return 2, None
            if self.__gb.solved and moves <= self.__target_moves:
                return 0, awards
            if self.__gb.solved and moves > self.__target_moves:
                return 1, awards

            # random event when target < moves < max
            if self.__target_moves < moves < max_moves:
                event_name, points_change = self.__generate_random_event()
                if event_name == 'None':
                    continue
                if points_change == 0: # blinded block event
                    if blind_event_counter >= self.__difficulty - 2:
                        continue
                    blind_event_counter += 1
                    self.__display_random_event((event_name, points_change))
                    blinded_blocks = random.choices(range(1, self.__difficulty ** 2), k=2)
                    continue

                # other random events
                self.__display_random_event((event_name, points_change))
                awards.append((event_name, points_change))

            self.__update_labels(blinded_blocks)

    def __update_labels(self, blinded: list[int] | None = None):
        """
        Create labels representing the game board. Blinded numbers will be displayed as '**'.
        """
        blinded = blinded if blinded is not None else []

        # create labels if there isn't any
        if len(self.__board_labels) == 0:
            for item in self.__gb.board:
                x_start = (self.get_control('dw_main').width - 4 - self.__difficulty * 6 - 25 - 1) // 2 + 2 # exclude divider
                y_start = (self.get_control('dw_main').height - 4 - self.__difficulty * 3) // 2 + 2
                x, y = item
                text = f'{self.__gb.board[item]:0>2}' if self.__gb.board[item] not in blinded else '**'
                lbl_block = TxtLabel(f'lbl_block:{x};{y}', 6, 3, x_start + x * 6, y_start + y * 3,
                                     text=text, draw_borders=True,
                                     border_colour=ForegroundColours.MAGENTA,
                                     padding_top=1, padding_bottom=1, padding_left=2, padding_right=2)
                lbl_block.formatted_text.set_format(0, slice(2), lbl_block.border_colour)
                if lbl_block.text == '00':
                    lbl_block.text = '  '
                self.__board_labels[item] = lbl_block
            self.get_control('dw_main').controls.extend(list(self.__board_labels.values()))
            return

        # update existing
        for x, y in self.__gb.board:
            num = self.__gb.board[(x, y)]
            lbl = self.__board_labels[(x, y)]
            lbl_text = f'{num:0>2}' if num not in blinded else '**'
            lbl.text = lbl_text if num != 0 else '  '
        self.render()

    def __generate_random_event(self) -> tuple[str, int]:
        """
        Get a random event (either award or penalties). Higher difficulty level should have larger possibility
        of awards than of penalties.
        :return: a rewards tuple
        """
        events = (
            ('None', 0),
            ('A witch used a spell on you! Some of the blocks are now hidden from you!', 0),
            ('A golden coin was hidden under the block! You sold it for 100 points!', 100),
            ('An angel blessed you! +500 points!', 500),
            ('A sneaky mouse stole 100 points from you! :-(', -100),
            ('Bad luck! A witch cursed you! -300 points! @#%$!', -300),
        )
        bad_events_weight = self.__difficulty / (self.__difficulty + self.__difficulty ** 2)
        good_events_weight = 1 - bad_events_weight
        event_weights = (
            75, # None
            5,  # Blinded blocks
            good_events_weight * 20 * 0.8, # Golden coin
            good_events_weight * 20 * 0.2, # Angel
            bad_events_weight * 20 * 0.8, # Mouse
            bad_events_weight * 20 * 0.2, # Witch
        )
        event = random.choices(events, weights=event_weights, k=1)[0]
        return event

    def __display_random_event(self, event: tuple[str, int]):
        """
        Displays a dialogue and asks the user to reveal the random event.
        """
        dw_event = DialogueWindow('dw_event', 40, 15, 30, 10, title='??????', border_colour=ForegroundColours.CYAN)
        dw_event.controls.append(
            TxtLabel('lbl_back', 38, 13, 1, 1, text='\n'.join('?' * 38 for _ in range(13))) # backdrop
        )
        lbl_prompt = TxtLabel('lbl_prompt', 36, 1, 2, 2, text='RANDOM EVENT! Press enter to reveal.')
        lbl_prompt.formatted_text.set_format(0, slice(36), ForegroundColours.CYAN, BackgroundColours.WHITE, TextFormats.BOLD)
        dw_event.controls.append(lbl_prompt)

        self.show_dialogue(dw_event, None)
        safe_input()

        dw_event.controls.clear()
        self.render()
        time.sleep(2)

        arts = ASCIIArts()
        ascii_arts_map = {
            0: arts.WITCH_WAND,  # Blinded blocks
            100: arts.GOLDEN_COINS,  # Golden coin
            500: arts.ANGEL,  # Angel
            -100: arts.MOUSE,  # Mouse
            -300: arts.WITCH_WAND  # Witch
        }
        art = ascii_arts_map[event[1]]

        lbl_art = (TxtLabel('lbl_art', 38, 13, 1, 1,
                           text='\n'.join(art[i] for i in range(13))))
        lbl_art.formatted_text.copy_from(art)
        dw_event.controls.append(lbl_art)

        lbl_event_msg = TxtLabel('lbl_event_msg', 36, 1, 2, 2, 1, auto_size=True,
                                 text=event[0], padding_left=2, padding_right=2)
        [lbl_event_msg.formatted_text.set_format(i, slice(None),
                                                 ForegroundColours.GREEN if event[1] > 0 else ForegroundColours.RED)
         for i in range(len(lbl_event_msg.formatted_text))]
        dw_event.controls.append(lbl_event_msg)

        self.render()
        safe_input()
        self.controls.remove(dw_event)

    def __display_error(self, msg: str):
        """
        Displays an error message to the user with a dialogue window.
        """
        dw_error = DialogueWindow('dw_error', 40, 10, 30, 10, title='ERROR!', border_colour=ForegroundColours.RED)
        lbl_error = TxtLabel('lbl_error', 36, 8, 2, 2, text=msg, auto_size=True)
        lbl_error.text += '\n\nPress enter to continue.\nHint: type /quit to exit the game.'
        [lbl_error.formatted_text.set_format(i, slice(36), ForegroundColours.RED) for i in range(len(lbl_error.formatted_text))]
        dw_error.controls.append(lbl_error)
        self.show_dialogue(dw_error, lambda _: input())

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

        def slide(self, number: int):
            """
            Slides the block with the specified number.
            Validity of move should be checked before calling this method.
            """
            number_index = list(self.board.keys())[list(self.board.values()).index(number)]
            # swap
            self.board[number_index], self.board[self.__empty_index] = self.board[self.__empty_index], self.board[number_index]
            self.find_adjacent()
            self.__check_if_solved()

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

        def __check_if_solved(self):
            """
            Checks if the board has been solved. Result is stored in self.solved.
            """
            solved = True
            counter = 1
            for y in range(self.__difficulty):
                for x in range(self.__difficulty):
                    if x == self.__difficulty - 1 and y == self.__difficulty - 1:
                        solved = solved and self.board[(x, y)] == 0
                    else:
                        solved = solved and self.board[(x, y)] == counter
                    if not solved:
                        return
                    counter += 1
            self.solved = True
