from tui import Screen
import tui.transitions as transitions
import speed_slide.__game_consts as consts
from speed_slide.game_scenes import *
import random

from tui.transitions import scatter


def __random_transition():
    return random.choice((
        transitions.scatter(200),
        transitions.wipe_up_to_down,
        transitions.wipe_down_to_up,
        transitions.slide_from_top,
        transitions.slide_from_bottom,
    ))


def game():
    game_screen = Screen(consts.__SCREEN_WIDTH, consts.__SCREEN_HEIGHT)

    game_screen.transition_into_scene(InitScene(consts.__SCREEN_WIDTH, consts.__SCREEN_HEIGHT))
    game_screen.play_scene()

    game_screen.transition_into_scene(TitleScene(consts.__SCREEN_WIDTH, consts.__SCREEN_HEIGHT), transitions.scatter(200), 0.02)
    game_screen.play_scene()

    game_screen.transition_into_scene(MainGameMenu(consts.__SCREEN_WIDTH, consts.__SCREEN_HEIGHT), __random_transition(), 0.02)
    game_screen.play_scene()