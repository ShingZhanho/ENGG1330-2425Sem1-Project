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
        self.__is_content_modified = True

        self.__padding_left = kwargs.get('padding_left', 0)
        self.__padding_right = kwargs.get('padding_right', 0)
        self.__padding_top = kwargs.get('padding_top', 0)
        self.__padding_bottom = kwargs.get('padding_bottom', 0)
        self.__draw_borders = kwargs.get('draw_borders', False)
        self.__text = text
        self.__auto_size = kwargs.get('auto_size', False) # auto-resize label to fit all texts


    @property
    def auto_size(self):
        return self.__auto_size

    @auto_size.setter
    def auto_size(self, value):
        if self.__auto_size == value:
            return
        self.__auto_size = value
        self.__is_content_modified = True


    @property
    def draw_borders(self):
        return self.__draw_borders

    @draw_borders.setter
    def draw_borders(self, value):
        if self.padding_left == 0 or self.padding_right == 0 or self.padding_top == 0 or self.padding_bottom == 0:
            if self.__draw_borders:
                self.__is_content_modified = True
            self.__draw_borders = False
        else:
            if self.__draw_borders != value:
                self.__is_content_modified = True
            self.__draw_borders = value


    @property
    def padding_left(self):
        return self.__padding_left

    @padding_left.setter
    def padding_left(self, value):
        if self.__padding_left == value:
            return
        self.__padding_left = value
        self.__is_content_modified = True


    @property
    def padding_right(self):
        return self.__padding_right

    @padding_right.setter
    def padding_right(self, value):
        if self.__padding_right == value:
            return
        self.__padding_right = value
        self.__is_content_modified = True


    @property
    def padding_top(self):
        return self.__padding_top

    @padding_top.setter
    def padding_top(self, value):
        if self.__padding_top == value:
            return
        self.__padding_top = value
        self.__is_content_modified = True


    @property
    def padding_bottom(self):
        return self.__padding_bottom

    @padding_bottom.setter
    def padding_bottom(self, value):
        if self.__padding_bottom == value:
            return
        self.__padding_bottom = value
        self.__is_content_modified = True


    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if self.__text == value:
            return
        self.__text = value
        self.__is_content_modified = True


    def __process_text(self):
        # pre-process text for rendering
        self.__processed_text = []
        max_length = self.width - self.padding_left - self.padding_right
        if self.auto_size:
            # wraps text
            for line in self.__text.split('\n'):
                if line == '':
                    line = ' ' # preserve empty lines
                self.__processed_text.extend(textwrap.wrap(line, max_length, drop_whitespace=False))
            self.height = len(self.__processed_text) + self.padding_top + self.padding_bottom
        else:
            max_lines = self.height - self.padding_top - self.padding_bottom
            lines = self.__text.split('\n')
            for i in range(min(len(lines), max_lines)):
                self.__processed_text.append(lines[i][:max_length])

    def __try_get_processed_text(self, i, j):
        try:
            return self.__processed_text[i][j]
        except IndexError:
            return ' '


    def render(self):
        # performance optimisation: only re-render if content is modified
        if self._rendered is not None and not self.__is_content_modified:
            return

        self.__process_text()
        self._rendered = [''] * self.height
        for i in range(self.height):
            for j in range(self.width):
                # draw borders if enabled
                if self.draw_borders:
                    # corners
                    if i == 0 and j == 0:
                        self._rendered[i] = SingleBorders.UPPER_LEFT
                        continue
                    elif i == 0 and j == self.width - 1:
                        self._rendered[i] += SingleBorders.UPPER_RIGHT
                        continue
                    elif i == self.height - 1 and j == 0:
                        self._rendered[i] = SingleBorders.LOWER_LEFT
                        continue
                    elif i == self.height - 1 and j == self.width - 1:
                        self._rendered[i] += SingleBorders.LOWER_RIGHT
                        continue
                    # horizontal borders
                    elif i == 0 or i == self.height - 1:
                        self._rendered[i] += SingleBorders.UPPER_LOWER
                        continue
                    # vertical borders
                    elif j == 0 or j == self.width - 1:
                        self._rendered[i] += SingleBorders.LEFT_RIGHT
                        continue

                # draw padding
                if self.draw_borders:
                    if ((1 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 2) or
                            (1 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 2)):
                        self._rendered[i] += ' '
                        continue
                else:
                    if ((0 <= i <= self.padding_top - 1 or self.height - self.padding_bottom <= i <= self.height - 1) or
                            (0 <= j <= self.padding_left - 1 or self.width - self.padding_right <= j <= self.width - 1)):
                        self._rendered[i] += ' '
                        continue

                # draw text
                self._rendered[i] += self.__try_get_processed_text(i - self.padding_top, j - self.padding_left)
