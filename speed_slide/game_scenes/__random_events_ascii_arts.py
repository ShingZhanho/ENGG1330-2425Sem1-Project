from tui import RichFormatText, ForegroundColours, BackgroundColours


class EventASCIIArts:
            """
            ASCII Arts for random events. Each art should be 38 x 13 maximum.
            """

            def __init__(self):
                [self.WITCH_WAND.set_format(i, slice(38), ForegroundColours.YELLOW, BackgroundColours.DEFAULT) for i in range(13)]

            WITCH_WAND = RichFormatText(r"""




                 *  __o    
                 |_/_\_   
                 \(0_0)
                   ( )\
                   / \
======================================

""")
