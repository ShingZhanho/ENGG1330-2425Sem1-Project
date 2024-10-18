from tui import ForegroundColours as FColours, BackgroundColours as BColours, TextFormats as TFormats


class RichFormatText(object):
    """
    A class for providing support for coloured text and other effects.
    """

    def __init__(self, text: str):
        # constants
        self.__DEFAULT_FORMAT = (FColours.DEFAULT, BColours.DEFAULT, TFormats.DEFAULT)

        self.__lines: list[str] = text.replace('\r\n', '\n').split('\n')
        self.__format_options: list[list[tuple[int, int, int]]] = []
        self.clear_formats()

    def __len__(self) -> int:
        return len(self.__lines)

    def __getitem__(self, index: int) -> str:
        return self.__lines[index]

    def __setitem__(self, index: int, item: str):
        self.__lines = item

        # adjusts formatting options
        len_diff = len(item) - len(self.__format_options[index])
        if len_diff > 0: # longer than original text
            self.__format_options[index].extend(self.__DEFAULT_FORMAT for _ in range(len_diff + 1))
        elif len_diff < 0: # shorter than original text
            self.__format_options[index] = self.__format_options[index][:len_diff]

    def set_format(self, line: int, format_range: slice,
                   foreground: int = FColours.DEFAULT,
                   background: int = BColours.DEFAULT,
                   text_format: int = TFormats.DEFAULT) -> 'RichFormatText':
        """
        Sets the format options for a given range of text.
        """
        for i in range(*format_range.indices(len(self.__format_options[line]))):
            self.__format_options[line][i] = (foreground, background, text_format)
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
        return self.__format_options[line][*get_range.indices(len(self.__format_options))]

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

        for y in range(target_line, min(len(self.__lines), target_line + len(other))):
            line_of_other = y - target_line
            len_to_copy = min(len(other[line_of_other]), len(self.__lines[y]) - target_index)
            if copy_text:
                self.__lines[y] = (self.__lines[y][:target_index]
                                   + other[line_of_other][:len_to_copy]
                                   + self.__lines[y][target_index + len_to_copy:])
            if copy_formats:
                self.__format_options[y] = (self.__format_options[y][:target_index]
                                            + other.get_format(line_of_other, slice(0, len_to_copy, 1))
                                            + self.__format_options[y][target_index + len_to_copy:])

        return self

    def render(self) -> list[str]:
        output = []
        for i in range(len(self.__lines)):
            output_line = ''
            for index, (char, option) in enumerate(list(zip(self.__lines[i], self.__format_options[i]))):
                fg, bg, tf = option
                if index > 0 and self.__format_options[i][index - 1] == option:
                    output_line += char
                else:
                    output_line += f'\033[{tf};{fg};{bg}m{char}'
            output_line += '\033[0;39;49m' # ANSI code for resetting formats to default
            output.append(output_line)
        return output
