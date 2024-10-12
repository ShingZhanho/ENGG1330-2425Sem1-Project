from tui.controls import Control
from tui.controls.__border_tools import DoubleBorders
import time

class DialogueWindow(Control):
    """
    DialogueWindow is a pop-up window that displays customised controls and returns a value.
    """
    def __init__(self, width, height, x=0, y=0, z=0, title='New Dialogue', controls = []):
        super().__init__(max(width, 8), height, x, y, z)

        self.__rendered: str = None

        self.controls = controls
        self.title = title


    def render(self):
        """
        Renders the dialogue window.
        """
        output = [''] * self.height
        # always adjust width to be even
        if (self.width % 2) != 0:
            self.width += 1

        # handles title
        __MAX_TITLE_LENGTH = self.width - 6
        temp_title = self.title
        if len(self.title) > __MAX_TITLE_LENGTH:
            temp_title = self.title[:__MAX_TITLE_LENGTH-3] + '...' # truncate long title
        if (len(temp_title) % 2) != 0: # adjust title to be even
            temp_title += ' '
        temp_title = f'[{temp_title:^{len(temp_title)}}]'

        output[0] = (DoubleBorders.UPPER_LEFT + DoubleBorders.UPPER_LOWER * ((self.width - 2 - len(temp_title)) // 2)
                     + temp_title
                     + DoubleBorders.UPPER_LOWER * ((self.width - 2 - len(temp_title)) // 2) + DoubleBorders.UPPER_RIGHT)

        # draw borders
        for i in range(1, self.height-1):
            output[i] = DoubleBorders.LEFT_RIGHT + ' ' * (self.width - 2) + DoubleBorders.LEFT_RIGHT
        output[-1] = DoubleBorders.LOWER_LEFT + DoubleBorders.UPPER_LOWER * (self.width - 2) + DoubleBorders.LOWER_RIGHT

        # handles controls
        # sort controls, like in Scene
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        # render and draw controls
        for control in self.controls:
            control.render()
            for y in range(max(1, control.y_coord), min(self.height - 1, control.y_coord + control.height)):
                for x in range(max(1, control.x_coord), min(self.width - 1, control.x_coord + control.width)):
                    output[y] = output[y][:x] + control.draw(x-control.x_coord, y-control.y_coord) + output[y][x+1:]

        # convert output to string
        self.__rendered = '\n'.join(output)


    def draw(self, x, y) -> str:
        """
        Draw the dialogue window.
        """
        if self.__rendered is None:
            raise Exception('DialogueWindow cannot be drawn before rendering.')
        return self.__rendered.split('\n')[y][x]


    def show(self, func):
        """
        Display the dialogue and execute the function, returns the value.
        :param func: the function to execute during dialogue lifetime, takes the dialogue window as an argument for interaction
        :return: the value returned by the function
        """
        self.render()
        return func(self)


    def show(self, timeout: float):
        """
        Display the dialogue for a certain amount of time.
        :param timeout: the time to display the dialogue
        :return: None
        """
        self.render()
        time.sleep(timeout)
        return None