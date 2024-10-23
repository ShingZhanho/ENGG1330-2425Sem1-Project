from tui import Screen
import tui.transitions as transitions
from speed_slide.__game_consts import _Constants as Constants
from speed_slide.game_scenes import *
from speed_slide.__debug import DebugTools
from tui.controls import TxtLabel

__screen = Screen(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

def __get_arg(args: dict[str, str], keys: list[str], value_type: type, default_value):
    """
    Gets the value of command line arguments by key. Multiple keys can be specified (useful when shorthands are available).
    Only the last occurrence will be fetched when multiple keys are present.
    """
    value = None
    for key in keys:
        value = args.get(key, value if value is not None else str(default_value))

    # handle boolean:
    if value_type == bool:
        return value.lower() in ('true', '1', '')

    return value_type(value)

def __handle_launch_options(args: dict[str, str]):
    # debug mode
    Constants.DEBUG = __get_arg(args, ['--debug'], bool, False)

    # graphics options
    match __get_arg(args, ['--graphics-mode', '-g'], str, 'normal'):
        case 'normal':
            pass
        case 'performant':
            Constants.ANIMATION_SECONDS_PER_FRAME = 0.06

def __menu():
    __screen.transition_into_scene(MainGameMenuScene(), transitions.get_random(200), Constants.ANIMATION_SECONDS_PER_FRAME)
    return __screen.play_scene()

def __title():
    __screen.transition_into_scene(TitleScene(), time_per_frame=Constants.ANIMATION_SECONDS_PER_FRAME)
    __screen.play_scene()

def __about():
    __screen.transition_into_scene(AboutScene(), transitions.scatter(200), Constants.ANIMATION_SECONDS_PER_FRAME)
    __screen.play_scene()

def __start_new_game():
    difficulty = 3
    attempt = 1
    total_score = 0

    while True:
        __screen.transition_into_scene(GameLevelTitleScene(difficulty, attempt, total_score), transitions.scatter(200), Constants.ANIMATION_SECONDS_PER_FRAME)
        lbl_road: TxtLabel = __screen.play_scene() # the control is reused in the next scene

        main_scene = MainGameScene(difficulty, attempt)
        main_scene.add_control_at(lbl_road, lbl_road.x_coord, lbl_road.y_coord)
        __screen.transition_into_scene(main_scene, transitions.slide_from_right, Constants.ANIMATION_SECONDS_PER_FRAME)
        result, awards = __screen.play_scene() # refer to docstring of MainGameScene.play() for the return values

        if result == -1:
            break # stop immediately

        if result == 0: # advance to next level
            attempt = 1 if difficulty != 6 else attempt + 1
            difficulty = difficulty + 1 if difficulty < 6 else 6
        elif result == 1: # stay at same level
            attempt += 1

        if result == 0 or result == 1:
            summary_scene = LevelSummaryScene(total_score, awards, result == 0, difficulty == 6)
            summary_scene.add_control_at(lbl_road, lbl_road.x_coord, lbl_road.y_coord)
            __screen.transition_into_scene(summary_scene, transitions.slide_from_right, Constants.ANIMATION_SECONDS_PER_FRAME)
            total_score = __screen.play_scene() # LevelSummaryScene.play() returns the new total score

        if result == 2:
            __screen.transition_into_scene(GameOverScene(total_score), transitions.slide_from_right, Constants.ANIMATION_SECONDS_PER_FRAME)
            __screen.play_scene()
            break


def main(**kwargs):
    # configures debug tools
    Constants.DEBUG_TOOLS = DebugTools()

    __handle_launch_options(kwargs)

    __title()

    while True:
        user_option = __menu() # validity is ensured within MainGameMenu scene

        if user_option == 'Q':
            break
        elif user_option == 'N':
            __start_new_game()
        elif user_option == 'A':
            __about()

    __screen.transition_into_blank_scene(transitions.scatter(200), Constants.ANIMATION_SECONDS_PER_FRAME)
    __screen.clear_screen()
