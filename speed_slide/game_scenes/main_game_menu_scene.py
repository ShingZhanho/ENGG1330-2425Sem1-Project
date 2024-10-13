from tui import Scene
from tui.controls import *


class MainGameMenu(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)

        copyright_text = 'HKU ENGG1330 24/25 Semester 1 Group 1L3-3'
        lbl_copyright = TxtLabel(110, 3, 0, 0, text=f'{copyright_text: ^110}',
                                 padding_top=1, padding_bottom=1, padding_left=1, padding_right=1, draw_borders=True)
        self.controls.append(lbl_copyright)

        self.render()


    def play(self):
        menu_dw = DialogueWindow(60, 20, 25, 5, title="SpeedSlide Game Menu")
        menu_dw.controls.extend(
            [
                # header
                TxtLabel(50, 1, 5, 3, text='Select an option from the menu below:'),
                # menu options
                TxtLabel(50, 5, 5, 5, text='- [N]ew Game\n- [H]elp\n- [Q]uit', auto_size=True,
                         padding_top=1, padding_bottom=1, padding_left=1, padding_right=1, draw_borders=True),
                TxtLabel(50, 1, 5, 11, text='Only the first character of your input will be read.',
                         auto_size=True)
            ]
        )
        def get_user_input(scene: Scene):
            valid_inputs = ['N', 'H', 'Q']
            while True:
                user_option = input('Select an option: ').upper()[:1]
                if user_option.upper() in valid_inputs:
                    break

                # show error message
                invalid_option_dw = DialogueWindow(30, 10, 40, 8, title='ERROR!')
                invalid_option_dw.controls.append(
                    TxtLabel(28, 5, 1, 4, text=f'Option \"{user_option}\" is invalid! Please try again.',
                         padding_left = 2, padding_right = 2, auto_size=True)
                )
                scene.show_dialogue(invalid_option_dw, lambda _: input('Press any key to continue...'))

            return user_option

        operations = {
            'N': lambda: print('New Game'),
            'H': lambda: print('Help'),
            'Q': lambda: print('Quit')
        }
        menu_dw_output = self.show_dialogue(menu_dw, get_user_input)
        operations[menu_dw_output.upper()]()