"""
For trailer purposes.
Changes made on this branch must not be merged back to the master branch.
"""
import time

import tui
import tui.controls as controls
from tui import Scene


class LoadingScene(Scene):
    def __init__(self):
        super().__init__(110, 30)

        dw = controls.DialogueWindow('dw', 54, 7, 28, 11, title='ESTABLISHING CONNECTION...',
                                     border_colour=tui.ForegroundColours.GREEN)

        lbl_text = controls.TxtLabel('text', 50, 1, 2, 2,
                                     text="Hacking into HKU Grading System... (0%)")
        lbl_text.formatted_text.set_format(0, slice(None), tui.ForegroundColours.GREEN)

        dw.controls.append(lbl_text)

        lbl_pgbar = controls.TxtLabel('pgbar', 50, 1, 2, 4,
                                         text="[                                                ]")

        lbl_pgbar.formatted_text.set_format(0, slice(None), tui.ForegroundColours.GREEN)

        dw.controls.append(lbl_pgbar)

        self.controls.append(dw)

    def play(self):
        message = "Hacking into HKU Grading System..."
        time.sleep(0.5)

        lbl_text: controls.TxtLabel = self.get_control('dw').get_control('text')
        lbl_pgbar: controls.TxtLabel = self.get_control('dw').get_control('pgbar')

        for i in range(0, 81, 10):
            lbl_text.text = f"{message} ({i}%)"
            lbl_pgbar.text = '[' + f'{('#' * int(i / 100 * 48)): <48}' + ']'
            self.render()
            time.sleep(0.3)

        time.sleep(1)
        message = "Changing all grades to A+..."
        lbl_text.text = f'{message} (99%)'
        lbl_pgbar.text = '[' + ('#' * 47) + ' ]'
        self.render()
        time.sleep(1)

        return self.get_control('dw')