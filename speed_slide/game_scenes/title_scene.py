from tui import Scene, RichFormatText
from tui.controls import TxtLabel
import time


"""
The ASCII art for the game title:
 .d8888b.  8888888b.  8888888888 8888888888 8888888b.  
d88P  Y88b 888   Y88b 888        888        888  "Y88b 
Y88b.      888    888 888        888        888    888 
 "Y888b.   888   d88P 8888888    8888888    888    888 
    "Y88b. 8888888P"  888        888        888    888 
      "888 888        888        888        888    888 
Y88b  d88P 888        888        888        888  .d88P 
 "Y8888P"  888        8888888888 8888888888 8888888P"  
 
  .d8888b.  888      8888888 8888888b.  8888888888
d88P  Y88b 888        888   888  "Y88b 888        
Y88b.      888        888   888    888 888        
 "Y888b.   888        888   888    888 8888888    
    "Y88b. 888        888   888    888 888        
      "888 888        888   888    888 888        
Y88b  d88P 888        888   888  .d88P 888        
 "Y8888P"  88888888 8888888 8888888P"  8888888888 
"""


class TitleScene(Scene):
    def __init__(self, width, height):
        super().__init__(width, height)


    def play(self):
        # show animation for game title ASCII art
        lbl_speed = TxtLabel(56, 8, 0, 0, text=""" .d8888b.  8888888b.  8888888888 8888888888 8888888b.  
d88P  Y88b 888   Y88b 888        888        888  "Y88b 
Y88b.      888    888 888        888        888    888 
 "Y888b.   888   d88P 8888888    8888888    888    888 
    "Y88b. 8888888P"  888        888        888    888 
      "888 888        888        888        888    888 
Y88b  d88P 888        888        888        888  .d88P
 "Y8888P"  888        8888888888 8888888888 8888888P"  """)
        lbl_speed.formatted_text.set_random_colours_to_all()
        lbl_slide = TxtLabel(56, 8, 0, 0, text=""" .d8888b.  888      8888888 8888888b.  8888888888
d88P  Y88b 888        888   888  "Y88b 888        
Y88b.      888        888   888    888 888        
 "Y888b.   888        888   888    888 8888888    
    "Y88b. 888        888   888    888 888        
      "888 888        888   888    888 888
Y88b  d88P 888        888   888  .d88P 888
 "Y8888P"  88888888 8888888 8888888P"  88888888888""")
        lbl_slide.formatted_text.set_random_colours_to_all()

        self.add_control_at(lbl_speed, - lbl_speed.width - 1, 5)
        self.add_control_at(lbl_slide, self.width, 15)

        for i in range(-lbl_speed.width - 1, self.width + lbl_slide.width + 1, 4):
            self.controls[0].x_coord = i
            self.controls[1].x_coord = self.width - i - lbl_slide.width
            self.render()
            time.sleep(0.01)

        self.controls[0].x_coord = 27 # place at center
        self.controls[1].x_coord = 29
        self.render()

        time.sleep(2)

        self.controls.append(
            TxtLabel(110, 1, 0, 28,
                     text=f'{"Proudly presented by ENGG1330-1L3 Group 3.":^110}')
        )
        self.render()

        time.sleep(3)