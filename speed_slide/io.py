import string
from tui import *
from speed_slide.__game_consts import _Constants as Constants


def safe_input(prompt: RichFormatText = RichFormatText('>>> ')):
    """
    A safe version of the input() function that handles escape sequences properly.
    :param prompt: The prompt to display.
    :return: User input with only printable ASCII characters.
    """
    new_prompt = prompt

    if Constants.DEBUG:
        debug_prompt_phrase = 'YOU ARE IN [DEBUG] MODE. IF YOU DO NOT KNOW WHAT YOU ARE DOING, QUIT IMMEDIATELY.'
        new_prompt = RichFormatText(debug_prompt_phrase)

        debug_msg: RichFormatText = Constants.DEBUG_TOOLS.debug_msg
        if debug_msg is not None:
            new_prompt.append(debug_msg[0]).copy_from(debug_msg, 1, copy_text=False)

        (new_prompt.append(prompt[0])
              .set_format(0, slice(len(debug_prompt_phrase)), ForegroundColours.YELLOW, BackgroundColours.RED, TextFormats.BOLD)
              .copy_from(prompt, -1, 0, copy_text=False))

    print(new_prompt, end='', flush=True)
    user_in = input()

    output = ''
    # keep only printable characters
    for c in user_in:
        if c in string.printable:
            output += c

    return output