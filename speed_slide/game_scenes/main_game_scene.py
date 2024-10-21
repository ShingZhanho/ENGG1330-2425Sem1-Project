from tui import Scene
from tui.controls import TxtLabel, DialogueWindow
from speed_slide.__game_consts import _Constants as Constants


class MainGameScene(Scene):
    """
    The main game scene.
    """

    def __init__(self, difficulty: int, attempt: int, total_score: int):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)
