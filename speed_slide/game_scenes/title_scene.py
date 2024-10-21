from tui import Scene, RichFormatText, ForegroundColours
from tui.controls import TxtLabel
from speed_slide.__game_consts import _Constants as Constants
import time


class TitleScene(Scene):
    def __init__(self):
        super().__init__(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

    def play(self):
        except_colours = [ForegroundColours.BLACK, ForegroundColours.WHITE]

        # show animation for game title ASCII art
        lbl_speed = TxtLabel('lbl_speed', 56, 8, 0, 0, text=""" .d8888b.  8888888b.  8888888888 8888888888 8888888b.  
d88P  Y88b 888   Y88b 888        888        888  "Y88b 
Y88b.      888    888 888        888        888    888 
 "Y888b.   888   d88P 8888888    8888888    888    888 
    "Y88b. 8888888P"  888        888        888    888 
      "888 888        888        888        888    888 
Y88b  d88P 888        888        888        888  .d88P
 "Y8888P"  888        8888888888 8888888888 8888888P"  """)
        lbl_speed.formatted_text.set_random_colours_to_all(except_foreground=except_colours)
        lbl_slide = TxtLabel('lbl_slide', 56, 8, 0, 0, text=""" .d8888b.  888      8888888 8888888b.  8888888888
d88P  Y88b 888        888   888  "Y88b 888        
Y88b.      888        888   888    888 888        
 "Y888b.   888        888   888    888 8888888    
    "Y88b. 888        888   888    888 888        
      "888 888        888   888    888 888
Y88b  d88P 888        888   888  .d88P 888
 "Y8888P"  88888888 8888888 8888888P"  88888888888""")
        lbl_slide.formatted_text.set_random_colours_to_all(except_foreground=except_colours)

        self.add_control_at(lbl_speed, - lbl_speed.width - 1, 5)
        self.add_control_at(lbl_slide, self.width, 15)

        for i in range(-lbl_speed.width - 1, self.width + lbl_slide.width + 1, 10):
            lbl_speed.x_coord = i
            lbl_slide.x_coord = self.width - i - lbl_slide.width
            self.render()
            time.sleep(Constants.ANIMATION_SECONDS_PER_FRAME)

        lbl_speed.x_coord = 27 # place at center
        lbl_slide.x_coord = 29
        self.render()

        time.sleep(2)

        lbl_credits = TxtLabel('lbl_credits', 110, 1, 0, 28, text=f'{"Proudly presented by ENGG1330-1L3 Group 3.":^110}')
        lbl_credits.formatted_text.set_format(0, slice(110), ForegroundColours.YELLOW)
        self.controls.append(lbl_credits)
        self.render()

        time.sleep(3)