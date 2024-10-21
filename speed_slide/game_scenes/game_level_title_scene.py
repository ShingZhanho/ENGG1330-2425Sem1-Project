from tui import Scene
from speed_slide.__game_consts import _Constants as Constants


class GameLevelTitleScene(Scene):
    """
    The scene for displaying the title of a game level.
    """

    def __init__(self, level_difficulty: int, level_attempt: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)