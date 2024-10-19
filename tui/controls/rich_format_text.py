from tui.text_formats import ForegroundColours as FColours, BackgroundColours as BColours, TextFormats as TFormats


class RichFormatText(object):
    """
    A class for providing support for multi-line coloured text and other effects.
    """

    def __init__(self, text: str):
        """
        Creates a RichFormatText object. Line breaks are automatically converted to '\n', then handled automatically.
        """
        # constants
        self.__DEFAULT_FORMAT = (FColours.DEFAULT, BColours.TRANSPARENT, TFormats.DEFAULT)

        self.__lines: list[str] = text.replace('\r\n', '\n').split('\n')
        self.__format_options: list[list[tuple[int, int, int]]] = []
        self.clear_formats()

    @classmethod
    def create_by_size(cls, width: int, height: int, char: str = ' ') -> 'RichFormatText':
        """
        Creates a RichFormatText object with a blank canvas.
        """
        return RichFormatText('\n'.join([char * width for _ in range(height)]))

    def __len__(self) -> int:
        return len(self.__lines)

    def __getitem__(self, index: int) -> str:
        return self.__lines[index]

    def __setitem__(self, index: int, item: str):
        self.__lines[index] = item

        # adjusts formatting options
        len_diff = len(item) - len(self.__format_options[index])
        if len_diff > 0: # longer than original text
            self.__format_options[index].extend(self.__DEFAULT_FORMAT for _ in range(len_diff + 1))
        elif len_diff < 0: # shorter than original text
            self.__format_options[index] = self.__format_options[index][:len_diff]

    def __str__(self) -> str:
        return '\n'.join(self.render())

    def append(self, text: str) -> 'RichFormatText':
        """
        Appends a line to the end.
        """
        self.__lines.append(text)
        self.__format_options.append([self.__DEFAULT_FORMAT for _ in range(len(text))])
        return self

    def extend(self, lines: list[str]) -> 'RichFormatText':
        """
        Extends the text by appending multiple lines.
        """
        for line in lines:
            self.append(line)
        return self

    def copy(self) -> 'RichFormatText':
        """
        Returns a copy of the current RichFormatText object.
        """
        rft = RichFormatText('\n'.join(self.__lines))
        rft.__format_options = [line.copy() for line in self.__format_options]
        return rft

    def set_format(self, line: int, format_range: slice,
                   foreground: int | None = None,
                   background: int | None = None,
                   text_format: int | None = None) -> 'RichFormatText':
        """
        Sets the format options for a given range of text.
        """

        for i in range(*format_range.indices(len(self.__format_options[line]))):
            # keep original format if not specified
            foreground = self.__format_options[line][i][0] if foreground is None else foreground
            background = self.__format_options[line][i][1] if background is None else background
            text_format = self.__format_options[line][i][2] if text_format is None else text_format

            self.__format_options[line][i] = (foreground, background, text_format)
        return self

    def set_random_colours_to_all(self,
                                  random_foreground: bool = True,
                                  random_background: bool = False,
                                  avoid_colour_conflicts: bool = True) -> 'RichFormatText':
        """
        Sets random colours to all text.
        """
        for i in range(len(self.__lines)):
            for j in range(len(self.__lines[i])):
                avoid_conflict = avoid_colour_conflicts
                original_fg, original_bg, original_tf = self.__format_options[i][j]
                if original_bg == original_bg: # disable conflict avoidance if the original colours are already the same
                    avoid_conflict = False

                new_fg, new_bg = original_fg, original_bg
                if random_foreground:
                    new_fg = FColours.random()

                while True and random_background:
                    new_bg = BColours.random()
                    if avoid_conflict and new_bg != new_fg:
                        break

                self.__format_options[i][j] = (new_fg, new_bg, original_tf)
        return self

    def clear_formats(self) -> 'RichFormatText':
        """
        Resets all format options to default.
        """
        self.__format_options = []
        for line in self.__lines:
            self.__format_options.append([self.__DEFAULT_FORMAT for _ in range(len(line))])
        return self

    def get_format(self, line: int, get_range: slice) -> list[tuple[int, int, int]]:
        """
        Gets the formatting options of a specific line in a specific range.
        """
        return self.__format_options[line][get_range]

    def copy_from(self, other: 'RichFormatText', target_line: int = 0, target_index: int = 0,
                  copy_text = True, copy_formats = True) -> 'RichFormatText':
        """
        Copies the text and/or formatting options from another RichFormatText object and paste onto the current one.
        This does not change the dimensions of the original RichFormatText, i.e., anything outside the original
        RichFormatText will be ignored.
        :param other: The new RichFormatText object.
        :param target_line: The line to starting pasting.
        :param target_index: The horizontal index to start pasting.
        :param copy_text: Whether to copy text from the other RichFormatText.
        :param copy_formats: Whether to copy formatting options from the other RichFormatText.
        """
        if not copy_text and not copy_formats:
            return self
        if target_line >= len(self.__lines):
            return self

        for y in range(max(0, target_line), min(len(self), target_line + len(other))):
            r = range(max(0, target_index), min(len(self[y]), target_index + len(other[y - target_line])))
            if len(r) == 0:
                continue
            start_index, end_index = r.start, r.stop
            if copy_text:
                self[y] = self[y][:start_index] + other[y - target_line][start_index - target_index:end_index - target_index] + self[y][end_index:]
            if copy_formats:
                for x in r:
                    fg, bg, tf = other.__format_options[y - target_line][x - target_index]
                    if bg == BColours.TRANSPARENT: # handle transparent background
                        bg = self.__format_options[y][x][1]
                    self.set_format(y, slice(x, x + 1), fg, bg, tf)

        return self

    def render(self) -> list[str]:
        """
        Renders texts with ANSI control codes into list[str].
        """
        output = []
        for i in range(len(self.__lines)):
            output_line = ''
            for index, (char, option) in enumerate(list(zip(self.__lines[i], self.__format_options[i]))):
                fg, bg, tf = option
                if bg == BColours.TRANSPARENT:
                    bg = BColours.DEFAULT
                if index > 0 and self.__format_options[i][index - 1] == option:
                    output_line += char
                else:
                    output_line += f'\033[{tf};{fg};{bg}m{char}'
            output_line += '\033[0;39;49m' # ANSI code for resetting formats to default
            output.append(output_line)
        return output
