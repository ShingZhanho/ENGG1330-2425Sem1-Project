########## [ SPEED SLIDE README FILE for Player & Developer ] ##########

PART O: Introduction

This document consists of two parts: one for players and one for developers. You fill find information about how to
launch and play the game, the goal and aim of the game in the first part. The second part is more technical and is
intended for developers who would like to contribute or modify the game. This README provides only brief information
on the gameplay and its implementations behind the scene. For more detailed information, such as the reference for
our module TUI, please refer to the separate tech.md.


PART I: PLAYER'S HANDBOOK

1. Launching the game

    Before launching the game, you should ensure that your device fulfil the following prerequisites:
        - Has Python 3.11 or 3.12 installed
        - Has a terminal or console that can display at least 110 columns and 30 rows
        - Has a reasonably fast processor and enough memory for text-based UI rendering

    To launch the game, change to the directory where this handbook (readme.txt) is located and run the following command:
        $ python3 main.py

    SPEED SLIDE supports several command line options to modify its behaviour. For options that takes parameters, they
    are passed in the format of --option=value. The available options are:

        --graphics-mode=, -g=[normal|performant]
            Configures the graphics mode to use when playing animations in the game. The default mode is normal.
            Setting the mode to performant increases the time between each frame of an animation, hence slows down
            the rendering activity and alleviates glitching UI. Performant mode is useful when you are running
            the game on a remote terminal or a slow PC.

        --debug
            Enables debug mode. General players should NOT use this option. Debug mode is intended for developers only.
            Refer to PART II of this document for behaviours in DEBUG mode.

    Example usage:
        $ python3 main.py --graphics-mode=normal


2. Main Menu

    After the game title is displayed, the main menu is displayed. There are four options to choose from:

        [N]: New Game
            Start the game from level 1-1.

        [H]: Help
            Shows a step-by-step tutorial on how to play the game.

        [A]: About
            Displays information about the developer team and the version of the running game.

        [Q]: Quit
            Quits the game.

    To select an option, enter the letter marked in the square brackets, then press enter. The option letter
    is case-insensitive, meaning that entering both 'a' and 'A' will get you to the 'About' page. Only the
    first letter of your input is read by the program, meaning that entering 'Hello' will be treated as 'H'
    and gets you to the 'Help' page.


3. Gameplay

    Every game starts with a 3 x 3 board (difficulty 1). The numbers 1-8 are displayed on the board together with
    an empty box. The board will then be shuffled.

    GOAL: Solve the puzzle by sliding number blocks around to rearrange them into an ascending order from left to
    right, top to bottom.

    You may only slide the number block that is directly adjacent to the empty block into the empty block. Each
    time you slide, you are making a "move". Be careful, each level has a maximum number of moves, which is displayed
    on the right hand side of your game board. You lose the game if you cannot solve the puzzle within the maximum
    moves.

    Each time you solve a puzzle, you get certain amount of base points as rewards.

    If you solve the puzzle within the "target moves", you will get bonus points. Also, you are then promoted to the
    next difficulty level (4 x 4, 5 x 5, then 6 x 6 board).

    If you solve the puzzle above the target moves, you will only get base points and will stay on the same difficulty
    level. BE CAREFUL! When your total moves is between target moves and max moves, there will be random events
    happening sometimes. They might be giving you extra points, or stealing points from you, or just makes your game
    even more difficult by hiding random blocks from you.

    HINTS:
    At anytime during the game, type the command '/surrender' to give up the level and end the game. The game will then
    show you your final score.
    You may also type the command '/quit' to end the game immediately. YOU WILL NOT SEE YOUR FINAL SCORE WITH '/quit'
    AND YOUR FINAL SCORE WILL BE LOST.

    After the game ends, you will return to the main menu.

4. Troubleshooting

    If you experience glitching in animation...
    -  You may try to launch the game in performant graphics mode. See Part I.1 Launching the Game
       If the problem persists, it may imply the rendering speed of your device cannot fully support the games rendering.
       Try running the game on another device and avoid running the game from a remote terminal.

    If you cannot see the colours clearly...
    -  Colours of the terminal is configured and controlled by your terminal. SPEED SLIDE can do nothing
       to control the colours of your terminal. Please check your terminal's settings and change to another
       colour profile.


PART II: DEVELOPER'S HANDBOOK

SPEED SLIDE uses no third-party packages or libraries. It is implemented completely in native Python 3.12. There are
some core modules that are designed specifically for SPEED SLIDE.

1. TUI module

    TUI (Text/Terminal-based User Interface) is the backbone of SPEED SLIDE's UI. It was inspired by operas - it uses
    the concept of scenes to create a dynamic and complex UI. Here are the core components of the TUI module:

    - Screen (class)
        The Screen instance manages a virtual text-based screen on which scenes and their controls are rendered.
        Screen instances are initialised with a blank scene.

        Constructor:
        __init__(width: int, height: int)
            Creates a new Screen instance with the specified width and height.


        Methods:
        play_scene(self)
            Execute the play() method of the current scene and returns its result.
            Refer to documentations about Scene for more information.

        print_scene(self, scene: Scene = None)
            Prints the specified scene on the screen. If no scene is specified, the current scene is printed.

            Parameters:
                scene: Scene
                    The scene to be printed. Default = None

        transition_into_scene(self, scene: Scene, transition: callable, time_per_frame: float = 0.1)
            Transitions from the current scene to the target scene using the specified transition generator.

            Parameters:
                scene: Scene
                    The scene to transition into.
                transition: callable
                    The transition generator which takes the current scene and the target scene as arguments, and
                    generates a list of frames to be played as the transition.
                    There are built-in transitions in the TUI module under tui.transitions. Developers may also create
                    their own transitions.
                    Please also refer to documentations for tui.transitions.
                time_per_frame: float
                    The time in seconds to wait between each frame of the transition. Default = 0.1s

            Exceptions:
                - ValueError: raised when the scene is not of the same size as the screen


    - Scene (class)
        The Scene instance contains several controls that are either created at initialisation or added during its
        lifetime. Each scene has its own lifetime which is represented by the play() method.