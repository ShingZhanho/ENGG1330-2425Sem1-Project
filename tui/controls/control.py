from tui.controls.rich_format_text import RichFormatText

class Control:
    """
    The base class of all interactable controls.
    """
    def __init__(self, control_id: str, width: int, height: int, x_coord: int, y_coord: int, z_coord = 0):
        self.control_id = control_id
        self.width = width
        self.height = height
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.z_coord = z_coord # determines the overlapping relationship between controls

        self._internal_rft: RichFormatText | None = None

    def render(self):
        # the base control class does not render anything
        pass

    def get_rft_object(self) -> RichFormatText:
        """
        Gets the RichFormatText object that contains rendering information about the control.
        Meant to be used internally. The base class always returns None.
        """
        return self._internal_rft
