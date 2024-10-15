from tui.controls.control import Control
import textwrap
from tui.controls.__border_tools import SingleBorders


class TxtLabel(Control):
    """
    TxtLabel provides an environment for displaying text
    """
    def __init__(self, width, height, x = 0, y = 0, z = 0, text = '', **kwargs):
        super().__init__(width, height, x, y, z)

        self.__processed_text = []
        self.__rendered = None
        self.__is_content_modified = True

        self._padding_left = kwargs.get('padding_left', 0)
        self._padding_right = kwargs.get('padding_right', 0)
        self._padding_top = kwargs.get('padding_top', 0)
        self._padding_bottom = kwargs.get('padding_bottom', 0)
        self._draw_borders = kwargs.get('draw_borders', False)
        self._text = text
        self._auto_size = kwargs.get('auto_size', False) # auto-resize label to fit all texts


    @property
    def auto_size(self):
        return self._auto_size

    @auto_size.setter
    def auto_size(self, value):
        if self._auto_size == value:
            return
        self._auto_size = value
        self.__is_content_modified = True


    @property
    def draw_borders(self):
        return self._draw_borders

    @draw_borders.setter
    def draw_borders(self, value):
        if self.padding_left == 0 or self.padding_right == 0 or self.padding_top == 0 or self.padding_bottom == 0:
            if self._draw_borders:
                self.__is_content_modified = True
            self._draw_borders = False
        else:
            if self._draw_borders != value:
                self.__is_content_modified = True
            self._draw_borders = value


    @property
    def padding_left(self):
        return self._padding_left

    @padding_left.setter
    def padding_left(self, value):
        if self._padding_left == value:
            return
        self._padding_left = value
        self.__is_content_modified = True


    @property
    def padding_right(self):
        return self._padding_right

    @padding_right.setter
    def padding_right(self, value):
        if self._padding_right == value:
            return
        self._padding_right = value
        self.__is_content_modified = True


    @property
    def padding_top(self):
        return self._padding_top

    @padding_top.setter
    def padding_top(self, value):
        if self._padding_top == value:
            return
        self._padding_top = value
        self.__is_content_modified = True


    @property
    def padding_bottom(self):
        return self._padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        if self._padding_bottom == value:
            return
        self._padding_bottom = value
        self.__is_content_modified = True


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self._text = value
        self.__is_content_modified = True


    def __process_text(self):
        # pre-process text for rendering
        self.__processed_text = []
        max_length = self.width - self.padding_left - self.padding_right
        if self.auto_size:
            # break each line at spaces or hyphens
            for line in self._text.split('\n'):
                self.__processed_text.extend(textwrap.wrap(line, max_length))
            self.height = len(self.__processed_text) + self.padding_top + self.padding_bottom
        else:
            max_lines = self.height - self.padding_top - self.padding_bottom
            lines = self._text.split('\n')
            for i in range(min(len(lines), max_lines)):
                self.__processed_text.append(lines[i][:max_length])

    def __try_get_processed_text(self, i, j):
        try:
            return self.__processed_text[i][j]
        except IndexError:
            return ' '


    def render(self):
        # performance optimisation: only re-render if content is modified
        if self.__rendered is not None and not self.__is_content_modified:
            return

        self.__process_text()
        self.__rendered = [''] * self.height
        for i in range(self.height):
            for j in range(self.width):
                # draw borders if enabled
                if self.draw_borders:
                    # corners
                    if i == 0 and j == 0:
                        self.__rendered[i] = SingleBorders.UPPER_LEFT
                        continue
                    elif i == 0 and j == self.width - 1:
                        self.__rendered[i] += SingleBorders.UPPER_RIGHT
                        continue
                    elif i == self.height - 1 and j == 0:
                        self.__rendered[i] = SingleBorders.LOWER_LEFT
                        continue
                    elif i == self.height - 1 and j == self.width - 1:
                        self.__rendered[i] += SingleBorders.LOWER_RIGHT
                        continue
                    # horizontal borders
                    elif i == 0 or i == self.height - 1:
                        self.__rendered[i] += SingleBorders.UPPER_LOWER
                        continue
                    # vertical borders
                    elif j == 0 or j == self.width - 1:
                        self.__rendered[i] += SingleBorders.LEFT_RIGHT
                        continue

                # draw padding
                if self.draw_borders:
                    if ((1 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 2) or
                            (1 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 2)):
                        self.__rendered[i] += ' '
                        continue
                else:
                    if ((0 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 1) or
                            (0 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 1)):
                        self.__rendered[i] += ' '
                        continue

                # draw text
                self.__rendered[i] += self.__try_get_processed_text(i - self.padding_top, j - self.padding_left)


    def draw(self, x, y):
        return self.__rendered[y][x]
