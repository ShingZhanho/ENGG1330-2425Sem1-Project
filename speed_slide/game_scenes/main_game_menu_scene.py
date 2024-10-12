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
        menu_dw = DialogueWindow(60, 20, 25, 5, title="Speed Slide Game Menu")
        menu_dw.controls.extend(
            [
                # header
                TxtLabel(50, 1, 5, 3, text='Select an option from the menu below:'),
                # menu options
                TxtLabel(50, 5, 5, 5, text='- [N]ew Game\n- [H]elp\n- [Q]uit', auto_size=True,
                         padding_top=1, padding_bottom=1, padding_left=1, padding_right=1, draw_borders=True),
            ]
        )

        user_option = self.show_dialogue(menu_dw, lambda: input('Option: '))