from tui.controls import Control
from tui.controls import DialogueWindow
from tui.controls.rich_format_text import RichFormatText


class Scene(object):
    """
    The basic class for a scene.
    """

    def __init__(self, width: int, height: int, background: RichFormatText = RichFormatText(' '),
                 background_tile_offset: int = 0):
        self.__rendered = None
        self._internal_rft: RichFormatText | None = None

        self.background = background
        self.background_tile_offset = background_tile_offset
        self.controls: list[Control] = []  # list of controls in the scene
        self.width = width
        self.height = height
        self.on_scene_update: callable = None

    def __get_tiled_background(self) -> RichFormatText:
        tile_pattern_len = len(self.background[0])
        canvas = RichFormatText((self.background[0] * (self.width // tile_pattern_len + 1))[:self.width])
        for y in range(self.height):
            offset = y * self.background_tile_offset % tile_pattern_len
            canvas.append((self.background[0][offset:] + self.background[0] * (self.width // tile_pattern_len))[:self.width])
        return canvas

    def register_scene_update_hook(self, func: callable):
        """
        Register a function to be called when the scene is updated.
        """
        self.on_scene_update = func

    def remove_scene_update_hook(self):
        """
        Remove the function that is called when the scene is updated.
        """
        self.on_scene_update = None

    def add_control_at(self, control: Control, x: int, y: int):
        """
        Add a control at a specific position rather than its original position.
        """
        control.x_coord = x
        control.y_coord = y
        self.controls.append(control)
        self.render()

    def play(self):
        """
        The method for starting the scene.
        """
        return None  # default scene output

    def render(self, suppress_hook: bool = False):
        """
        Render the scene.
        """
        self._internal_rft = self.__get_tiled_background()

        # sort controls by z-index, lowest first, then by y-coordinate, and then by x-coordinate
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        for control in self.controls:
            control.render()
            self._internal_rft.copy_from(control.get_rft_object(), control.y_coord, control.x_coord)

        if self.on_scene_update is not None and not suppress_hook:
            self.on_scene_update(self)

    def get_rendered(self, force_rerender: bool = False, suppress_hook: bool = False) -> list[str]:
        """
        Get the list representation of the rendered scene.
        :param force_rerender: Force the scene to be re-rendered.
        :param suppress_hook: Suppress the scene update hook.
        :return: The list representation of the rendered scene.
        """
        if force_rerender or self._internal_rft is None:
            self.render(suppress_hook=suppress_hook)
        return self._internal_rft.render()

    def draw(self, x, y):
        """
        Draw the scene.
        """
        if self.__rendered is None:
            raise Exception('Scene cannot be drawn before rendering.')
        return self.__rendered.split('\n')[y][x]

    def show_dialogue(self, dialogue: DialogueWindow, func: callable):
        """
        Show a dialogue window. Ask for user input and return the result.
        """
        dialogue.z_coord = max(self.controls, key=lambda c: c.z_coord).z_coord + 1
        self.controls.append(dialogue)
        self.render()
        result = func(self)
        self.controls.remove(dialogue)
        self.render()
        return result
