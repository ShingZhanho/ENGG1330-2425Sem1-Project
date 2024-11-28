> [!Note]
> **[ARCHIVED REPOSITORY]**
> Following the end of the course, this repository has been archived and is no
> longer maintained.

# Related Videos
| Demonstration                                                                                              | Trailer                                                                                                    |
|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| [![YouTube](http://i.ytimg.com/vi/7Z3sSEoryKM/hqdefault.jpg)](https://www.youtube.com/watch?v=7Z3sSEoryKM) | [![YouTube](http://i.ytimg.com/vi/Kz2ZYzK26N4/hqdefault.jpg)](https://www.youtube.com/watch?v=Kz2ZYzK26N4) |

# SpeedSlide Manual for Players and Developers

## Table of Contents
> 1. [Introduction](#0x00-introduction)
> 2. [Instructions for Players](#0x01-instructions-for-players)
>   - [System Requirements and Prerequisites](#1-system-requirements-and-prerequisites)
>   - [Launching the Game](#2-launching-the-game)
>   - [Main Menu](#3-main-menu)
>   - [Gameplay](#4-gameplay)
>   - [Troubleshooting](#5-troubleshooting)
> 3. [Instructions for Developers](#0x02-instructions-for-developers)
>   - [Build](#1-build)
>   - [Debug Mode](#2-debug-mode)
>   - [Project Structure](#3-project-structure)
>   - [Game Mechanics](#4-game-mechanics)
## `0x00` Introduction

This document consists of two parts: one for players and one for developers.
You will find information about how to launch and play the game, the goal and 
aim of the game in the first part. The second part is more technical and is
intended for developers who would like to contribute or modify the game.
This README provides only brief information on the gameplay and its 
implementations behind the scene.

## `0x01` Instructions for Players

### 1 System Requirements and Prerequisites

To run the game, you should ensure that you have:
- Python 3.11 or 3.12 installed. (Other versions may work, but they are not 
tested.)
- A terminal emulator that supports `ANSI` escape codes. (`Windows Terminal` is
the suggested terminal emulator on Windows.)
- A terminal emulator that can display at least 110 columns and 33 rows.

### 2 Launching the Game

To launch the game, change the working directory to where `main.py` is located,
activate a virtual environment (recommended, create one if there isn't any),
then simply run the script `main.py`. An example is shown:
```bash
$ cd /path/to/speedslide/files/
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ python3 main.py
```

#### Command Line Arguments

SpeedSlides accepts several command line arguments to modify the game's
behaviour. The following is a reference of the available arguments:

> **`--debug`**
> 
> **Intended for developers' use only. Normal players should not use this
> option.**
> 
> Enables debug mode. This was mainly used during development stage. Most of
> its functionalities have been removed in the final version. However, it still
> modifies certain game behaviours. You should refer to the developer's section
> for more details.

> **`--graphics-mode=, -g=[normal | performant]`**
> 
> Choose the graphics mode to use for the game. The `performant` mode will
> reduce the framerate of certain animations to improve performance on slower
> devices. This is useful when running the game from a remote terminal like
> the Ed platform.
> 
> **Default: `normal`**

Example usage:
```bash
$ python3 main.py --graphics-mode=performant
```

### 3 Main Menu

After the title animation, you are presented with the main menu. You may
choose from one of the following options:

- **[H]ow to play**: Displays the help information.
    Provides introduction to the game's
    goal and how you may control it. There are also useful tricks and tips in
    the help section. You should read them if this is your first time playing
    SpeedSlide.
- **[N]ew Game**: Starts the game from level 1-1.
- **[A]bout**: Displays the information about the game development team.
- **[Q]uit**: Leaves the game.

You can select an option by entering the corresponding key, followed by enter.
The menu will only read the first character you enter. For example, entering
`Hello, World!` will take you to the help section.

### 4 Gameplay

Please refer to the help section built into the game for more information.
Gameplay is not explained here to reduce redundancy.

### 5 Troubleshooting

1. **If you experience glitching in animation...**
    - Try running the game in `performant` mode. This will reduce the framerate
        of certain animations to improve performance.
    - If you are running the game from a remote terminal, try running the game
        locally instead.

2. **If you cannot see the colours clearly...**

    SpeedSlide uses standard ANSI escape codes to display colours. Actual
    colours are controlled by your terminal emulator. If you cannot see the
    colours clearly, you may need to adjust the colour settings in your
    terminal emulator. Sometimes, adjusting the accessibility settings of
    your system may also help.


## `0x02` Instructions for Developers

### 1 Build

SpeedSlide requires only standard Python without any dependencies, and is
readily runnable when you have all files properly placed.

### 2 Debug Mode

Debug mode is enabled by the `--debug` command line argument. When you are
in debug mode, there will be a prompt displayed at the bottom of the screen
indicating so.

The following debug mode exclusive features are included in the original
code:
- **Simplified board shuffling**: The board will only be shuffled for 3 moves
    regardless of the random target moves generated during runtime. This
    makes solving the puzzle easier for debugging purposes.
- **`/pass-a` command during gameplay**: This command skips the current level
    and make the game think that the player passed the level above the target
    moves (i.e. the player will stay on the same level).
- **`/pass-b` command during gameplay**: This command skips the current level
    and make the game think that the player passed the level below the target
    moves (i.e. the player will be promoted to the next level).
- **`/fail` command during gameplay**: This command fails the current level
    and the game should show the 'Game Over' screen.

If you wish to add more debug mode exclusive codes, you can check the flag
`speed_slide.__game_consts._Constants.DEBUG`. The type of the value is 
boolean.

### 3 Project Structure

This is an overview of the project's files. Note that the structure of
`tui` is not shown here. For more information about the `tui` module, please
refer to the separate file at `./tui/README.md`.

```
speed_slide/
├── __game_consts.py
├── __init__.py
├── io.py
└── game_scenes/
    ├── __init__.py
    ├── __random_events_ascii_arts.py
    ├── about_scene.py
    ├── game_level_title_scene.py
    ├── game_over_scene.py
    ├── goodbye_scene.py
    ├── help_scene.py
    ├── level_summary_scene.py
    ├── main_game_menu_scene.py
    ├── main_game_scene.py
    ├── title_scene.py
    └── customised_controls/
        ├── __init__.py
        └── score_label.py
```

Major and important classes and functions are documented here.

NOTE: This is not an exhaustive list of all classes and functions. Only those
that are significant are documented here. For other classes and functions,
refer to the docstrings in the source code.

> #### File `speed_slide/__game_consts.py`)
>
> **Class `_Constants`**
> - Although named "Constants", the value of the members can be modified
>   during runtime, especially at launch. However, this is not recommended
>   to do so during runtime.
> - Intended for internal use only.
> - Members:
>   - `ANIMATION_SECONDS_PER_FRAME: float` - The duration between each frame
>     of the animations. Measured in seconds. Default: `0.02` if in normal
>     graphics mode, `0.06` if in performant mode.
>   - `DEBUG: bool` - Whether the game is in debug mode. Default: `False`.
>   - `SCREEN_HEIGHT: int` - The height of the game screen. Default: `30`.
>   - `SCREEN_WIDTH: int` - The width of the game screen. Default: `110`.
>   - `VERSION_STRING: str` - The version of the game.

> #### File `speed_slide/__init__.py`
> 
> **Method `main(**kwargs): -> None`**
> - Entry point exposed to the outside.
> - `**kwargs` takes the **processed** command line arguments in the form
>   of `dict[key, value]`.

> #### File `speed_slide/io.py`
> 
> **Method `beep(): -> None`**
> - Produces a beep sound by printing the ASCII bell character.
> 
> **Method `safe_input(prompt: RichFormatText): -> str`**
> - A safe implementation of the built-in `input()` function.
> - `prompt` is the rich-formatted prompt displayed before the cursor.
>       Multi-line prompts are supported.
> - Returns the processed user input. Only printable ASCII characters are
>       included in the return value.

> #### File `speed_slide/game_scenes/__random_events_ascii_arts.py`
> 
> **Class `EventASCIIArts`**
> 
> Contains ASCII arts used in random events. This class should only be used
> internally. Refer to the source code for the ASCII arts and 
> `speed_slide/game_scenes/main_game_scene.py` for information
> on random events.

> #### File `speed_slide/game_scenes/about_scene.py`
> 
> **Class `AboutScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the information about the game development team is shown.

> #### File `speed_slide/game_scenes/game_level_title_scene.py`
> 
> **Class `GameLevelTitleScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the title of the current level is shown.

> #### File `speed_slide/game_scenes/game_over_scene.py`
> 
> **Class `GameOverScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the 'Game Over' message is shown.

> #### File `speed_slide/game_scenes/goodbye_scene.py`
> 
> **Class `GoodbyeScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the goodbye message is shown. Displayed when the player
>   quits the game.

> #### File `speed_slide/game_scenes/help_scene.py`
> 
> **Class `HelpScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the help information is shown.

> #### File `speed_slide/game_scenes/level_summary_scene.py`
> 
> **Class `LevelSummaryScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - A scene on which the summary of the game level is shown. Information
>   are regarding the bonus points and total points the player has earned.

> #### File `speed_slide/game_scenes/main_game_menu_scene.py`
> 
> **Class `MainGameMenuScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - The main menu that is displayed upon successful launch of the game.

> #### File `speed_slide/game_scenes/main_game_scene.py`
> 
> **Class `MainGameScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - This is where the game UI and game logic are implemented.
> 
> **Class `__GameBoard`**
> - An internal class that represents the game board and provides several
>   useful methods for interacting with the board.

> #### File `speed_slide/game_scenes/title_scene.py`
> 
> **Class `TitleScene`**
> - Object inheritance: `object` -> `tui.scene.Scene`
> - The ASCII art of the title "SpeedSlide" is animated and displayed in
>   this scene.

> #### File `speed_slide/game_scenes/customised_controls/score_label.py`
> 
> **Class `ScoreLabel`**
> - Object inheritance: `object` -> `tui.controls.Control`
> - A customised control that supports display and animating an integer score
>   for up to 10 digits (positive, 9 digits if negative).
> - Although it uses an internal `TxtLabel` control, it does not inherit from
>   it and hence they do not share the same members.

### 4 Game Mechanics

The game is implemented through an internal class `__GameBoard`. The class
stores the board's status in the format of `dict[tuple[int, int], int]`,
where the key of the dictionary is the coordinates of the number block, and
the value being the number.

At the start of each level, a new `__GameBoard` is created, which contains
a game board in its solved state. Then, the board is shuffled. To ensure
solvability, shuffling always starts with the initial state of a solved
board. The `slide()` function of `__GameBoard` is called to slide a certain
block into the empty space for several times.

To find the blocks that are available for sliding, a method `find_adjacent()`
can be called. The function looks up the four possible locations, namely the
blocks above, below, on the left of, on the right of the empty space. The
results are stored in `__GameBoard.adjacent`, which is a list. The maximum
possible length of the list is 4, since adjacent blocks can be less than 4
when the empty space is at the edges.

Each time the `slide()` function is called, it will check whether the block
the player is trying to slide is within `__GameBoard.adjacent`, and make the
move if the slide is possible. `True` is returned for a successful slide, and
`False` otherwise.

Every time the board is updated, `__check_if_solved()` is called to check
whether the board has been solved. And the main game loop will use this
information to determine whether to exit the loop and return the results.