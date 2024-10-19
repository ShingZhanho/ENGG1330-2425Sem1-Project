from tui import Scene
from tui.controls import TxtLabel
from tui import RichFormatText
import time


class InitScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height, RichFormatText('=+'), background_tile_offset=1)

        # prepare controls
        self.controls.append(
            TxtLabel(50, 3, 30, 11,
                     text=f'{"Initialising Game ...": ^40}',
                     padding_top=1, padding_bottom=1, padding_left=5, padding_right=5, draw_borders=True, auto_size=True)
        )


    def play(self):
        self.render()
        time.sleep(2)


