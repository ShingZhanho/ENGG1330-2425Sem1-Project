"""
txt_label control provides an environment for displaying text
"""

from tui.controls.control import Control
import textwrap
from tui.controls.__border_tools import SingleBorders


class TxtLabel(Control):
    def __init__(self, width, height, x = 0, y = 0, z = 0, text = '', **kwargs):
        super().__init__(width, height, x, y, z)

        self.__processed_text = []
        self.__pre_rendered = []

        self.padding_left = kwargs.get('padding_left', 0)
        self.padding_right = kwargs.get('padding_right', 0)
        self.padding_top = kwargs.get('padding_top', 0)
        self.padding_bottom = kwargs.get('padding_bottom', 0)
        self.draw_borders = kwargs.get('draw_borders', False)
        self._text = text
        self._auto_size = kwargs.get('auto_size', False) # auto-resize label to fit all texts


    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        self._auto_size = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    @property
    def draw_borders(self):
        return self._draw_boarder

    @draw_borders.setter
    def draw_borders(self, value):
        if self.padding_left == 0 or self.padding_right == 0 or self.padding_top == 0 or self.padding_bottom == 0:
            self._draw_boarder = False
        else:
            self._draw_boarder = value


    def __process_text(self):
        # pre-process text for rendering
        self.__processed_text = []
        max_length = self.width - self.padding_left - self.padding_right
        if not self.auto_size:
            max_lines = self.height - self.padding_top - self.padding_bottom
            lines = self._text.split('\n')
            for i in range(min(len(lines), max_lines)):
                self.__processed_text.append(lines[i][:max_length])
        else:
            # break each line at spaces or hyphens
            for line in self._text.split('\n'):
                self.__processed_text.extend(textwrap.wrap(line, max_length))
            self.height = len(self.__processed_text) + self.padding_top + self.padding_bottom


    def __try_get_processed_text(self, i, j):
        try:
            return self.__processed_text[i][j]
        except IndexError:
            return ' '


    def render(self):
        self.__process_text()
        self.__pre_rendered = [''] * self.height
        for i in range(self.height):
            for j in range(self.width):
                # draw borders if enabled
                if self.draw_borders:
                    # corners
                    if i == 0 and j == 0:
                        self.__pre_rendered[i] = SingleBorders.UPPER_LEFT
                        continue
                    elif i == 0 and j == self.width - 1:
                        self.__pre_rendered[i] += SingleBorders.UPPER_RIGHT
                        continue
                    elif i == self.height - 1 and j == 0:
                        self.__pre_rendered[i] = SingleBorders.LOWER_LEFT
                        continue
                    elif i == self.height - 1 and j == self.width - 1:
                        self.__pre_rendered[i] += SingleBorders.LOWER_RIGHT
                        continue
                    # horizontal borders
                    elif i == 0 or i == self.height - 1:
                        self.__pre_rendered[i] += SingleBorders.UPPER_LOWER
                        continue
                    # vertical borders
                    elif j == 0 or j == self.width - 1:
                        self.__pre_rendered[i] += SingleBorders.LEFT_RIGHT
                        continue

                # draw padding
                if self.draw_borders:
                    if ((1 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 2) or
                            (1 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 2)):
                        self.__pre_rendered[i] += ' '
                        continue
                else:
                    if ((0 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 1) or
                            (0 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 1)):
                        self.__pre_rendered[i] += ' '
                        continue

                # draw text
                self.__pre_rendered[i] += self.__try_get_processed_text(i - self.padding_top, j - self.padding_left)


    def draw(self, x, y):
        return self.__pre_rendered[x][y]
