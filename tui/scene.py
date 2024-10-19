from tui.controls import Control
from tui.controls import DialogueWindow
from tui.controls.rich_format_text import RichFormatText


class Scene(object):
    """
    The basic class for a scene.
    """

    def __init__(self, width: int, height: int, background: str = ' '):
        self.__rendered = None
        self._internal_rft: RichFormatText | None = None

        self.background = background
        self.background_rft = RichFormatText.create_by_size(width, height, background)
        self.controls: list[Control] = []  # list of controls in the scene
        self.width = width
        self.height = height
        self.on_scene_update: callable = None

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
        self._internal_rft = RichFormatText.create_by_size(self.width, self.height, self.background)
        self._internal_rft.copy_from(self.background_rft)

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

    def get_rft(self, force_rerender: bool = False, suppress_hook: bool = False) -> RichFormatText:
        """
        Get the RichFormatText object of the rendered scene.
        :param force_rerender: Force the scene to be re-rendered.
        :param suppress_hook: Suppress the scene update hook.
        :return: The RichFormatText object of the rendered scene.
        """
        if force_rerender or self._internal_rft is None:
            self.render(suppress_hook=suppress_hook)
        return self._internal_rft

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
