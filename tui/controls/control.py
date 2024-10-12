"""
The base class of all interactable controls.
"""

class Control():
    def __init__(self, width: int, height: int, x_coord: int, y_coord: int, z_coord = 0):
        self.width = width
        self.height = height
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord # determines the overlapping relationship between controls

        self._rendered = [' ' * self.width] * self.height

    def render(self):
        # the base control class does not render anything
        pass

    def draw(self, x, y) -> str:
        return self._rendered[x][y]