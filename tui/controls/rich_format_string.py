import random
from enum import IntEnum


class BgColours(IntEnum):
    """
    Enum shortcuts for ANSI background colour codes.
    """
    BLACK = 40,
    RED = 41,
    GREEN = 42,
    YELLOW = 43,
    BLUE = 44,
    MAGENTA = 45,
    CYAN = 46,
    WHITE = 47,
    DEFAULT = 49,


class FgColours(IntEnum):
    """
    Enum shortcuts for ANSI foreground colour codes.
    """
    BLACK = 30,
    RED = 31,
    GREEN = 32,
    YELLOW = 33,
    BLUE = 34,
    MAGENTA = 35,
    CYAN = 36,
    WHITE = 37,
    DEFAULT = 39,


class TextFormats(IntEnum):
    """
    Enum shortcuts for ANSI text formatting codes.
    Only those that are commonly implemented are available.
    """
    DEFAULT = 0,
    BOLD = 1,
    ITALIC = 3,
    UNDERLINE = 4,


def rfs(string: str) -> 'RichFormatString':
    """
    Shortcut for creating a RichFormatString object from string.
    :param string: The string to apply formatting settings.
    :return: A RichFormatString object.
    """
    return RichFormatString(string)


class RichFormatString(object):
    """
    A class for providing support for coloured text and other decorations.
    """

    def __init__(self, string: str):
        """
        Creates a new RichFormatString object.
        The text of RichFormatString is immutable but the formatting can be modified.
        :param string: The string to apply formatting settings.
        """
        self.__string = string
        self.__format = [(FgColours.DEFAULT, BgColours.DEFAULT, TextFormats.DEFAULT)] * len(string)

        self.__RESET_FORMAT = f'\033[{TextFormats.DEFAULT};{BgColours.DEFAULT};{FgColours.DEFAULT}m'

    def apply_format(self,
                     start_index: int = 0,
                     end_index: int = None,
                     step: int = 1,
                     fg_colours: FgColours = FgColours.DEFAULT,
                     bg_colours: BgColours = BgColours.DEFAULT,
                     text_format: TextFormats = TextFormats.DEFAULT) -> 'RichFormatString':
        """
        Applies formats to the string in the specified range (entire string by default).
        Range is specified like you would when slicing a string, i.e. [start_index:end_index:step].
        :param start_index: Index of the first character to apply the colour to.
        :param end_index: Index of the character after the last character to apply the colour to.
        :param step: Step size for the range.
        :param fg_colours: The ANSI foreground colour code. Use FgColours to get supported values.
        :param bg_colours: The ANSI background colour code. Use BgColours to get supported values.
        :param text_format: The text formatting code. Use TextFormats to get supported values.
        :return: The RichFormatString object itself for chaining.
        """
        if end_index is None:
            end_index = len(self.__string)
        for i in range(start_index, end_index, step):
            self.__format[i] = (fg_colours, bg_colours, text_format)
        return self

    def apply_random_formats(self,
                             start_index: int = 0,
                             end_index: int = None,
                             step: int = 1,
                             random_fg_colours: bool = True,
                             random_bg_colours: bool = False,
                             random_text_format: bool = False,
                             avoid_colour_conflict: bool = True) -> 'RichFormatString':
        """
        Applies random formats to the string in the specified range.
        :param start_index: Index of the first character to apply the random formats to.
        :param end_index: Index of the character after the last character to apply the random formats to.
        :param step: Step size for the range.
        :param random_fg_colours: Whether to apply random foreground colours.
        :param random_bg_colours: Whether to apply random background colours.
        :param random_text_format: Whether to apply random text formats.
        :param avoid_colour_conflict: Whether to avoid colour conflicts between foreground and background colours.
        :return: The RichFormatString object itself for chaining.
        """
        fg_colours = list(FgColours)
        bg_colours = list(BgColours)
        text_formats = list(TextFormats)
        if end_index is None:
            end_index = len(self.__string)
        for i in range(start_index, end_index, step):
            fg_colours = random.choice(fg_colours) if random_fg_colours else self.__format[i][0]

            while True:
                bg_colours = random.choice(bg_colours) if random_bg_colours else self.__format[i][1]
                if ((not avoid_colour_conflict or (self.__format[i][0] - 30) == (self.__format[i][1] - 40)) or
                        (fg_colours - 30) != (bg_colours - 40)):
                    # keep trying until the colours are different if avoid_colour_conflict is True
                    # or ignore avoid_colour_conflict if the original background and foreground colours are already the same
                    break

            text_formats = random.choice(text_formats) if random_text_format else self.__format[i][2]

            self.__format[i] = (fg_colours, bg_colours, text_formats)
        return self

    def clear_formats(self) -> 'RichFormatString':
        """
        Removes all formatting options.
        :return: The RichFormatString object itself for chaining.
        """
        self.__format = [None] * len(self.__string)
        return self

    def get_char_for_printing(self, index: int) -> str:
        """
        Get the character at the specified index along with the ANSI formatting codes.
        :param index: The index of the character.
        :return: The character with its formatting codes at the specified index.
        """
        return f'\033[{self.__format[index][2]};{self.__format[index][1]};{self.__format[index][0]}m{self.__string[index]}\033[0m'

    def __str__(self) -> str:
        string = ''
        for i, char in enumerate(self.__string):
            formats = self.__format[i]
            # if the format remains the same, do not reset and do not include new format codes
            if i > 0 and formats == self.__format[i - 1]:
                string += char
            else:
                string += f'{self.__RESET_FORMAT}\033[{formats[2]};{formats[1]};{formats[0]}m{char}'
        # resets the format at the end
        string += self.__RESET_FORMAT
        return string
