from tui import *
from tui.controls import *
from speed_slide.io import safe_input


class AboutScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height, ' ')

        [self.background_rft.set_format(y, slice(width), background=BackgroundColours.CYAN) for y in range(height)]

    def play(self):
        return safe_input()