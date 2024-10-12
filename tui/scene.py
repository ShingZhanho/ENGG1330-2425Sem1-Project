from tui import Control


class Scene(object):
    """
    The basic class for a scene.
    """
    def __init__(self):
        self.__rendered = None

        self.controls: list[Control] = [] # list of controls in the scene


    def play(self):
        """
        The method for starting the scene.
        """
        return None # default scene output

    def render(self, width: int, height: int, background: str = ' '):
        """
        Render the scene.
        :param width: the width of the scene
        :param height: the height of the scene
        :param background: the character to fill the background of the scene
        """
        temp = [[None for _ in range(width)] for _ in range(height)]
        # sort controls by z-index, lowest first, then by y-coordinate, and then by x-coordinate
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        for control in self.controls:
            control.render()
            for y in range(max(0, control.y_coord), min(height, control.y_coord + control.height)):
                for x in range(max(0, control.x_coord), min(width, control.x_coord + control.width)):
                    # draw the control on temp canvas
                    temp[y][x] = control.draw(x-control.x_coord, y-control.y_coord)

        # replace None with spaces
        for y in range(len(temp)):
            for x in range(len(temp[y])):
                if temp[y][x] is None:
                    temp[y][x] = background

        # convert temp canvas to string
        self.__rendered = '\n'.join([''.join(row) for row in temp])


    def draw(self, x, y):
        """
        Draw the scene.
        """
        if self.__rendered is None:
            raise Exception('Scene cannot be drawn before rendering.')
        return self.__rendered.split('\n')[y][x]