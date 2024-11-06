"""
For trailer purposes.
Changes made on this branch must not be merged back to the master branch.
"""
import time

import tui
import tui.controls as controls
from tui import Scene


class ADScene(Scene):
    def __init__(self, dw):
        super().__init__(110, 30)

        self.controls.append(dw)

        dw_red = controls.DialogueWindow('dw_red', 30, 10, 40, 10, 1, title='X  FATAL ERROR',
                                         border_colour=tui.ForegroundColours.RED)

        lbl_text = controls.TxtLabel('txt', 26, 1, 2, 1, auto_size=True,
                                     text="""ACCESS DENIED (0x00001330)
--------------------------
MESSAGE FROM SERVER:

Connection blocked by Admin Dirk. Case reported to HKU Disciplinary Committee.""")
        [lbl_text.formatted_text.set_format(i, slice(None), tui.ForegroundColours.MAGENTA) for i in range(0, len(lbl_text.formatted_text))]

        dw_red.controls.append(lbl_text)

        self.controls.append(dw_red)

    def play(self):
        pass