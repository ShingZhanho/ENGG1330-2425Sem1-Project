from tui.controls import Control
from tui.controls import DialogueWindow


class Scene(object):
    """
    The basic class for a scene.
    """
    def __init__(self, width: int, height: int, background: str = ' '):
        self.__rendered = None

        self.background = background
        self.controls: list[Control] = [] # list of controls in the scene
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


    def play(self):
        """
        The method for starting the scene.
        """
        return None # default scene output

    def render(self):
        """
        Render the scene.
        """
        temp = [[None for _ in range(self.width)] for _ in range(self.height)]
        # sort controls by z-index, lowest first, then by y-coordinate, and then by x-coordinate
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        for control in self.controls:
            control.render()
            for y in range(max(0, control.y_coord), min(self.height, control.y_coord + control.height)):
                for x in range(max(0, control.x_coord), min(self.width, control.x_coord + control.width)):
                    # draw the control on temp canvas
                    temp[y][x] = control.draw(x-control.x_coord, y-control.y_coord)

        # replace None with spaces
        for y in range(len(temp)):
            for x in range(len(temp[y])):
                if temp[y][x] is None:
                    temp[y][x] = self.background

        # convert temp canvas to string
        self.__rendered = '\n'.join([''.join(row) for row in temp])

        if self.on_scene_update is not None:
            self.on_scene_update(self)


    def draw(self, x, y):
        """
        Draw the scene.
        """
        if self.__rendered is None:
            raise Exception('Scene cannot be drawn before rendering.')
        return self.__rendered.split('\n')[y][x]


    def show_dialogue(self, dialogue: DialogueWindow, func: callable = lambda: input('>>> ')):
        """
        Show a dialogue window. Ask for user input and return the result.
        """
        dialogue.z_coord = max(self.controls, key=lambda c: c.z_coord).z_coord + 1
        self.controls.append(dialogue)
        self.render()
        result = func()
        self.controls.remove(dialogue)
        self.render()
        return result