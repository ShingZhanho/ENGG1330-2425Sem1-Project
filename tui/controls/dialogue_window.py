from tui.controls import Control
from tui.controls.__border_tools import DoubleBorders
from tui.controls.rich_format_text import RichFormatText
from tui.text_formats import ForegroundColours as FColours
import time

class DialogueWindow(Control):
    """
    DialogueWindow is a pop-up window that displays customised controls and returns a value.
    """
    def __init__(self, control_name, width, height, x=0, y=0, z=0, title='New Dialogue', **kwargs):
        super().__init__(control_name, max(width, 8), height, x, y, z)

        self.controls = []
        self.title = title
        self.border_colour = kwargs.get('border_colour', FColours.DEFAULT)


    def render(self):
        """
        Renders the dialogue window.
        """
        self._internal_rft = RichFormatText.create_by_size(self.width, self.height)
        # always adjust width to be even
        if (self.width % 2) != 0:
            self.width += 1

        # draw controls
        # sort controls, like in Scene
        self.controls.sort(key=lambda c: (c.z_coord, c.y_coord, c.x_coord))
        # render and draw controls
        for control in self.controls:
            control.render()
            self._internal_rft.copy_from(control.get_rft_object(), control.y_coord, control.x_coord)

        # handles title
        max_title_len = self.width - 6
        temp_title = self.title
        if len(temp_title) > 0:
            if len(self.title) > max_title_len:
                temp_title = self.title[:max_title_len-3] + '...' # truncate long title
            if (len(temp_title) % 2) != 0: # adjust title to be even
                temp_title += ' '
            temp_title = f'[{temp_title:^{len(temp_title)}}]'

        self._internal_rft[0] = (DoubleBorders.UPPER_LEFT + DoubleBorders.UPPER_LOWER * ((self.width - 2 - len(temp_title)) // 2)
                     + temp_title
                     + DoubleBorders.UPPER_LOWER * ((self.width - 2 - len(temp_title)) // 2) + DoubleBorders.UPPER_RIGHT)

        # draw borders
        for i in range(1, self.height-1):
            self._internal_rft[i] = DoubleBorders.LEFT_RIGHT + self._internal_rft[i][1:-1] + DoubleBorders.LEFT_RIGHT
        self._internal_rft[-1] = DoubleBorders.LOWER_LEFT + DoubleBorders.UPPER_LOWER * (self.width - 2) + DoubleBorders.LOWER_RIGHT

        # applies formatting for borders
        (self._internal_rft.set_format(0, slice(self.width), foreground=self.border_colour)
         .set_format(-1, slice(self.width), foreground=self.border_colour))
        for i in range(1, self.height-1):
            (self._internal_rft.set_format(i, slice(1), foreground=self.border_colour)
             .set_format(i, slice(-1, self.width), foreground=self.border_colour))

    def get_control(self, control_id: str) -> Control:
        """
        Gets the control with the specified control_id.
        """
        for control in self.controls:
            if control.control_id == control_id:
                return control
        raise ValueError(f'\'{self.control_id}\' does not contain a child control \'{control_id}\'.')

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