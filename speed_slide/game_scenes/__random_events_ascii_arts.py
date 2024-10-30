from tui import RichFormatText, ForegroundColours, BackgroundColours


class EventASCIIArts:
            """
            ASCII Arts for random events. Each art should be 38 x 13 maximum.
            """

            def __init__(self):
                self.WITCH_WAND = RichFormatText(r"""



                 Ω
                 v  __o    
                 |_/_\_   
                 \ (X)
                  `( )\
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

                self.ANGEL = RichFormatText(r"""
                
                
                
                   -=-   
                (\  _  /)
                ( \( )/ )       
                (       )
                 `>   <´   
                 /     \ 
    Pinterest    ,     , 
    @lexisoniat   ¯._.¯  
""")
                # Credit: Pinterest @lexisoniat (https://www.pinterest.com/pin/394065036117525960/
                [self.ANGEL.set_format(i, slice(None), ForegroundColours.GREEN, BackgroundColours.DEFAULT) for i in range(13)]

                self.MOUSE = RichFormatText(r"""
                
                
                

        
                ~Ω8> 
          ~Ω8>          <8Ω~
                 ~Ω8>
           ~Ω8>    <8Ω~   ~Ω8> 
        <8Ω~
                  ~Ω8>    <8Ω~
""")
                [self.MOUSE.set_format(i, slice(None), ForegroundColours.RED, BackgroundColours.DEFAULT) for i in range(13)]

