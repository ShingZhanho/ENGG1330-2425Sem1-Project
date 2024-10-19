from tui.controls.control import Control
import textwrap
from tui.controls.__border_tools import SingleBorders
from tui.text_formats import ForegroundColours as FColours
from tui.controls.rich_format_text import RichFormatText


class TxtLabel(Control):
    """
    TxtLabel provides an environment for displaying text
    """

    def __init__(self, control_name, width, height, x=0, y=0, z=0, text='', **kwargs):
        super().__init__(control_name, width, height, x, y, z)

        self.__is_content_modified = True

        self.__padding_left = kwargs.get('padding_left', 0)
        self.__padding_right = kwargs.get('padding_right', 0)
        self.__padding_top = kwargs.get('padding_top', 0)
        self.__padding_bottom = kwargs.get('padding_bottom', 0)
        self.__draw_borders = kwargs.get('draw_borders', False)
        self.__border_colour = kwargs.get('border_colour', FColours.DEFAULT)
        self.__text = text
        self.__auto_size = kwargs.get('auto_size', False)  # auto-resize label to fit all texts
        self.__formatted_text = RichFormatText(text)

        self.__process_text()

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
    def border_colour(self):
        return self.__border_colour

    @border_colour.setter
    def border_colour(self, value):
        if self.__border_colour == value:
            return
        self.__border_colour = value
        self.__is_content_modified = True

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
        self.__process_text()
        self.__is_content_modified = True

    @property
    def formatted_text(self):
        return self.__formatted_text

    def __process_text(self):
        # copy old formats
        old_formats = self.__formatted_text

        # pre-process text for rendering
        max_length = self.width - self.padding_left - self.padding_right
        if self.auto_size:
            # wraps text
            wrapped_lines = []
            for line in self.__text.split('\n'):
                if line == '':
                    line = ' '  # preserve empty lines
                wrapped_lines.extend(textwrap.wrap(line, max_length, drop_whitespace=False))
            self.height = len(wrapped_lines) + self.padding_top + self.padding_bottom
            self.__formatted_text = RichFormatText('\n'.join(wrapped_lines))
        else:
            max_lines = self.height - self.padding_top - self.padding_bottom
            self.__formatted_text = RichFormatText.create_by_size(max_length, max_lines)
            lines = self.__text.split('\n')
            for i in range(min(len(lines), max_lines)):
                self.__formatted_text[i] = lines[i][:max_length]

        # apply original formats
        self.__formatted_text.copy_from(old_formats, 0, 0, copy_text=False)

    def render(self):
        # performance optimisation: only re-render if content is modified
        if self._internal_rft is not None and not self.__is_content_modified:
            return

        self.__process_text()
        self._internal_rft = RichFormatText.create_by_size(self.width, self.height)

        # draw borders
        if self.draw_borders:
            self._internal_rft[0] = SingleBorders.UPPER_LEFT + SingleBorders.UPPER_LOWER * (self.width - 2) + SingleBorders.UPPER_RIGHT
            self._internal_rft[self.height - 1] = SingleBorders.LOWER_LEFT + SingleBorders.UPPER_LOWER * (self.width - 2) + SingleBorders.LOWER_RIGHT
            for i in range(1, self.height - 1):
                self._internal_rft[i] = SingleBorders.LEFT_RIGHT + ' ' * (self.width - 2) + SingleBorders.LEFT_RIGHT

        # draw text
        self._internal_rft.copy_from(self.__formatted_text, self.padding_top, self.padding_left)

        # apply formatting for borders
        if self.draw_borders:
            (self._internal_rft.set_format(0, slice(0, self.width), self.border_colour)
             .set_format(self.height - 1, slice(0, self.width), self.border_colour))
            for i in range(1, self.height - 1):
                self._internal_rft.set_format(i, slice(0, self.width), self.border_colour)
