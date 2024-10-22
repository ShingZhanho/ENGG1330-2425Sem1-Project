from tui import RichFormatText, ForegroundColours, BackgroundColours


class EventASCIIArts:
            """
            ASCII Arts for random events. Each art should be 38 x 13 maximum.
            """

            def __init__(self):
                self.WITCH_WAND = RichFormatText(r"""




                 *  __o    
                 |_/_\_   
                 \(0_0)
                   ( )\
                   / \
======================================

""")
                [self.WITCH_WAND.set_format(i, slice(38), ForegroundColours.MAGENTA, BackgroundColours.DEFAULT) for i in range(13)]


                self.GOLDEN_COINS = RichFormatText(r"""                                       
                                      
           _-----_                    
       ,"¯         ¯",
      /      _|_      \               
     |      (_|_`      |              
     |      ,_|_)      |              
      \       |       /               
       ¯".         ."¯                
           ¯-----¯                    
                                      

""")
                [self.GOLDEN_COINS.set_format(i, slice(None), ForegroundColours.YELLOW, BackgroundColours.DEFAULT) for i in range(13)]
