import time
from tui import *
from tui.controls import *
from speed_slide.io import safe_input
from speed_slide.__game_consts import _Constants as Constants


class AboutScene(Scene):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, ' ')

        [self.background_rft.set_format(y, slice(self.width)) for y in range(self.height)]

        # title
        lbl_title = TxtLabel('lbl_title', 50, 3, 0, 1, 0, f'{"Meet the Team~":^46}',
                             padding_top=1, padding_left=2, padding_right=2, padding_bottom=1, draw_borders=True, border_colour=ForegroundColours.BLUE)
        (lbl_title.formatted_text
         .set_format(0, slice(46), foreground=ForegroundColours.WHITE)
         .set_format(0, slice(16, 30), text_format=TextFormats.UNDERLINE))
        self.add_control_at(lbl_title, lbl_title.x_coord, lbl_title.y_coord)

        # version string
        lbl_version = TxtLabel('lbl_version', 40, 3, 70, 1, 0, f'Version: {Constants.VERSION_STRING}',
                                 padding_top=1, padding_left=4, padding_right=4, padding_bottom=1, draw_borders=True, border_colour=ForegroundColours.CYAN)
        lbl_version.formatted_text.set_format(0, slice(30), foreground=ForegroundColours.WHITE)
        self.add_control_at(lbl_version, lbl_version.x_coord, lbl_version.y_coord)

    def play(self):
        info_card_jacob = TxtLabel('info_card_jacob', 80, 6, -81, 4, 0, r"""
    ( )   SHING, Zhan Ho Jacob
  -(   )- BEng 28' | jacobszh@connect.hku.hk | 3036228892
    / \   Coding (TUI module, Game Logic)""", padding_left=2, padding_right=2, padding_top=1, padding_bottom=1,
                                   draw_borders=True, border_colour=ForegroundColours.GREEN)

        info_card_eason = TxtLabel('info_card_eason', 80, 6, -81, 10, 0, r"""    ( )
    -|-   LIU, Jialin (Eason)
     |    BEng 28' | u3639149@connect.hku.hk | 3036391493
    / \   Docs (Developer's Handbook) | Game Design""", padding_left=2, padding_right=2, padding_top=1, padding_bottom=1,
                                   draw_borders=True, border_colour=ForegroundColours.RED)

        info_card_rid = TxtLabel('info_card_rid', 80, 6, -81, 16, 0, r"""
    ( )   THANT, Kyaw Win (Rid)
   └(‡)┘  BEng 28' | u3645886@connect.hku.hk | 3036458863
    / \   Game Design | Project Video | Docs (Player's Handbook)""", padding_left=2, padding_right=2, padding_top=1, padding_bottom=1,
                                   draw_borders=True, border_colour=ForegroundColours.MAGENTA)

        info_card_david = TxtLabel('info_card_david', 80, 6, -81, 22, 0, r"""
    ( )   WU, Jun Hao (David)
    -|-   BEng 28' | u3638850@connect.hku.hk | 3036388501
    / \   Testing | Project Video""", padding_left=2, padding_right=2, padding_top=1, padding_bottom=1,
                                   draw_borders=True, border_colour=ForegroundColours.YELLOW)

        cards = [info_card_jacob, info_card_eason, info_card_rid, info_card_david]
        target_x_coords = (0, 10, 20, 30)
        for card in cards:
            [card.formatted_text
             .set_format(y, slice(0, 10), foreground=card.border_colour) # colour stick men
             .set_format(y, slice(10, None, None), foreground=ForegroundColours.WHITE) for y in range(0, 4)] # colour text
            card.formatted_text.set_format(1, slice(10, None, None), foreground=card.border_colour, text_format=TextFormats.UNDERLINE_AND_BOLD) # underline name

        self.controls.extend(cards)
        self.render()

        # cards entrance animation
        for x in range(-81, max(target_x_coords) + 6, 6):
            for card, target_x in list(zip(cards, target_x_coords)):
                card.x_coord = min(x, target_x)
            self.render()
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

        safe_input(RichFormatText('Press enter to return to the main menu...'))

        # cards exit animation
        for x in range(1, 110 + 6, 6):
            for card in cards:
                card.x_coord = card.x_coord if x < card.x_coord else x
            self.render()
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

        # clear controls
        self.controls.clear()
        self.render()
