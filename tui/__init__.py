import string

from tui.scene import Scene
from tui.screen import Screen
import tui.transitions as transitions
from tui.text_formats import ForegroundColours, BackgroundColours, TextFormats
from tui.controls.rich_format_text import RichFormatText


def safe_input(prompt: RichFormatText = RichFormatText('>>> ')):
    """
    A safe version of the input() function that handles escape sequences properly.
    :param prompt: The prompt to display.
    :return: User input with only printable ASCII characters.
    """
    print(prompt, end='', flush=True)
    user_in = input()

    output = ''
    # keep only printable characters
    for c in user_in:
        if c in string.printable:
            output += c

    return output
