"""
This is a file created for production of the game trailer video.
All changes made on this branch must not be merged back to the master branch.
"""
import tui
from trailer_vid.loading_scene import LoadingScene
from trailer_vid.access_denied_scene import ADScene


if __name__ == '__main__':
    screen = tui.Screen(110, 30)
    screen.clear_screen()
    input()

    screen.transition_into_scene(LoadingScene(), tui.transitions.wipe_up_to_down, 0.04)
    dw = screen.play_scene()

    screen.transition_into_scene(ADScene(dw), tui.transitions.wipe_up_to_down, 0.04)
    screen.play_scene()

    input()
