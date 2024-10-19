import string
from tui import *
from speed_slide.__game_consts import _Constants as Constants


def safe_input(prompt: RichFormatText = RichFormatText('>>> ')):
    """
    A safe version of the input() function that handles escape sequences properly.
    :param prompt: The prompt to display.
    :return: User input with only printable ASCII characters.
    """
    if Constants.DEBUG:
        debug_prompt_phrase = 'YOU ARE IN [DEBUG] MODE. IF YOU DO NOT KNOW WHAT YOU ARE DOING, QUIT IMMEDIATELY.'
        prompt = (RichFormatText(debug_prompt_phrase)
                  .append(prompt[0])
                  .set_format(0, slice(len(debug_prompt_phrase)), ForegroundColours.YELLOW, BackgroundColours.RED, TextFormats.BOLD)
                  .copy_from(prompt, 1, 0))
    print(prompt, end='', flush=True)
    user_in = input()

    output = ''
    # keep only printable characters
    for c in user_in:
        if c in string.printable:
            output += c

    return output