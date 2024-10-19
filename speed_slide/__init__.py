from tui import Screen
import tui.transitions as transitions
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.game_scenes import *
import random


__screen = Screen(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

def __get_arg(args: dict[str, str], keys: list[str], value_type: type, default_value):
    """
    Gets the value of command line arguments by key. Multiple keys can be specified (useful when shorthands are available).
    Only the last occurrence will be fetched when multiple keys are present.
    """
    value = None
    for key in keys:
        value = args.get(key, value if value is not None else default_value)

    # handle boolean:
    if value_type == bool:
        return value.lower() in ('true', '1', '')

    return value_type(value)

def __random_transition():
    return random.choice((
        transitions.scatter(200),
        transitions.wipe_up_to_down,
        transitions.wipe_down_to_up,
        transitions.slide_from_top,
        transitions.slide_from_bottom,
    ))

def __handle_launch_options(args: dict[str, str]):
    # debug mode
    Constants.DEBUG = __get_arg(args, ['--debug'], bool, False)

    # graphics options
    match __get_arg(args, ['--graphics-mode', '-g'], str, 'normal'):
        case 'normal':
            pass
        case 'performant':
            Constants.SCENE_TRANSITION_SECONDS_PER_FRAME = 0.06

def __menu():
    __screen.transition_into_scene(MainGameMenu(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), __random_transition(), Constants.SCENE_TRANSITION_SECONDS_PER_FRAME)
    return __screen.play_scene()

def __title():
    __screen.transition_into_scene(TitleScene(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), time_per_frame=Constants.SCENE_TRANSITION_SECONDS_PER_FRAME)
    __screen.play_scene()

def __about():
    __screen.transition_into_scene(AboutScene(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), transitions.scatter(200), Constants.SCENE_TRANSITION_SECONDS_PER_FRAME)
    __screen.play_scene()

def main(**kwargs):
    __handle_launch_options(kwargs)

    __title()

    while True:
        user_option = __menu() # validity is ensured within MainGameMenu scene

        if user_option == 'Q':
            break
        elif user_option == 'A':
            __about()

    __screen.clear_screen()
