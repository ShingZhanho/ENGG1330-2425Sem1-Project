########## [ SPEED SLIDE Handbook for Player & Developer ] ##########

PART O: Introduction

This document consists of two parts: one for players and one for developers. You fill find information about how to
launch and play the game, the goal and aim of the game in the first part. The second part is more technical and is
intended for developers who would like to contribute or modify the game.


PART I: PLAYER'S HANDBOOK

1. Launching the game

    Before launching the game, you should ensure that your device fulfill the following prerequisites:
        - Has Python 3.12 installed
        - Has a terminal or console that can display at least 110 columns and 30 rows
        - Has a reasonably fast processor and enough memory for text-based UI rendering

    To launch the game, change to the directory where this handbook (readme.txt) is located and run the following command:
        python3 main.py

    * Note: [GLITCHY UI]
            If you are using a remote terminal, you may experience glitching in the UI, especially when there are animations.
            This is due to the latency in the network and constant updates to the terminal. To avoid this, it is recommended
            that you run the game on a local terminal.


2. Gameplay

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