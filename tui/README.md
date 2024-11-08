                                     # TUI Package Documentation

This documentation provides information and guidance on how to use the TUI package.

## `tui` Module

### Members

#### `Screen` Class

- **Object inheritance**: `object` -> `Screen`
- **Description**: The `Screen` class creates an instance that manages the display
of scenes. It is recommended to share a single `Screen` instance across the entire
life cycle of your application.

##### Constructor `Screen()`

```python
def __init__(self, screen_width: int, screen_height: int)
```

**Description**\
Initializes a new `Screen` instance.

**Parameters**
- `screen_width` (`int`): The width of the screen in characters.
- `screen_height` (`int`): The height of the screen in characters.

##### Method `transition_into_scene()`

```python
def transition_into_scene(self, new_scene: Scene, transition: callable = transitions.direct, time_per_frame: float = 0.1)
```

**Description**\
Transitions from the current scene into the `new_scene` using the specified
`transition` generator function.
> **Note**\
> If the `scene` has its `exit_transition` property set as non-`None`, it will
> override the specified `transition` generator function.

**Parameters**
- `new_scene` (`Scene`): The scene to transition into.
- `transition` (`callable -> list[str]`): The transition generator function.
The function should return a list of strings, in which each string element
is what will be printed on the screen for each frame of the transition, with
all the ANSI escape sequences included, if any.
- `time_per_frame` (`float`): The time in seconds to wait between playing
each frame of the transition. Default is `0.1`.