"""
Contains generators of frames of transitions between two scenes.
"""

from tui import Scene
from tui.controls.rich_format_text import RichFormatText
import random


def __ensure_same_size(from_scene: Scene, to_scene: Scene):
    if from_scene.width != to_scene.width or from_scene.height != to_scene.height:
        raise ValueError('Scenes must be of the same size.')

def __get_rendered_tuple(s1: Scene, s2: Scene) -> tuple[list[str], list[str]]:
    # DEPRECATED. Kept for backward compatibility. Use __get_rendered_rft_tuple() instead.
    return s1.get_rendered(suppress_hook=True), s2.get_rendered(suppress_hook=True)

def __get_rendered_rft_tuple(s1: Scene, s2: Scene) -> tuple[RichFormatText, RichFormatText]:
    # New transitions should be implemented using this function instead of __get_rendered_tuple()
    return s1.get_rft(suppress_hook=True), s2.get_rft(suppress_hook=True)

def wipe_up_to_down(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the old scene is wiped from up to down by the new scene.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    from_scene_rendered, to_scene_rendered = __get_rendered_tuple(from_scene, to_scene)
    frames = []
    __ensure_same_size(from_scene, to_scene)
    for i in range(from_scene.height):
        frames.append('\n'.join(to_scene_rendered[:i + 1] + from_scene_rendered[i + 1:]))
    return frames

def wipe_down_to_up(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the old scene is wiped from down to up by the new scene.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    from_scene_rendered, to_scene_rendered = __get_rendered_tuple(from_scene, to_scene)
    frames = []
    __ensure_same_size(from_scene, to_scene)
    for i in range(from_scene.height, -1, -1):
        frames.append('\n'.join(from_scene_rendered[:i] + to_scene_rendered[i:]))
    return frames

def slide_from_top(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene slides from the top to the bottom.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    from_scene_rendered, to_scene_rendered = __get_rendered_tuple(from_scene, to_scene)
    frames = []
    __ensure_same_size(from_scene, to_scene)
    for i in range(to_scene.height):
        frames.append('\n'.join(to_scene_rendered[-(i + 1):] + from_scene_rendered[:from_scene.height - i - 1]))
    return frames

def slide_from_bottom(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene slides from the bottom to the top.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    from_scene_rendered, to_scene_rendered = __get_rendered_tuple(from_scene, to_scene)
    frames = []
    __ensure_same_size(from_scene, to_scene)
    for i in range(to_scene.height):
        frames.append('\n'.join(from_scene_rendered[i + 1:] + to_scene_rendered[:i + 1]))
    return frames

def slide_from_left(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene slides from the left to the right.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: All frames of the transition
    """
    from_scene_rft, to_scene_rft = __get_rendered_rft_tuple(from_scene, to_scene)
    __ensure_same_size(from_scene, to_scene)

    rft_frames = []

    for i in range(1, to_scene.width, 2):
        frame = RichFormatText.create_by_size(to_scene.width, to_scene.height)
        frame.copy_from(from_scene_rft, 0, i)
        frame.copy_from(to_scene_rft, 0, i - to_scene.width)
        rft_frames.append(frame)

    return ['\n'.join(rft.render()) for rft in rft_frames]

def slide_from_right(from_scene: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene slides from the right to the left.
    :param from_scene: The old scene
    :param to_scene: The new scene
    :return: All frames of the transition
    """
    from_scene_rft, to_scene_rft = __get_rendered_rft_tuple(from_scene, to_scene)
    __ensure_same_size(from_scene, to_scene)

    rft_frames = []

    for i in range(to_scene.width - 1, -1, -2):
        frame = RichFormatText.create_by_size(to_scene.width, to_scene.height)
        frame.copy_from(from_scene_rft, 0, i - to_scene.width)
        frame.copy_from(to_scene_rft, 0, i)
        rft_frames.append(frame)

    return ['\n'.join(rft.render()) for rft in rft_frames]

def scatter(chars_per_frame: int = 100) -> callable:
    """
    Constructs a scatter transition generator.
    :param chars_per_frame: Number of characters to scatter per frame.
    :return: The constructed scatter transition generator.
    """

    def inner_scatter(from_scene: Scene, to_scene: Scene) -> list[str]:
        from_scene_rft, to_scene_rft = __get_rendered_rft_tuple(from_scene, to_scene)
        __ensure_same_size(from_scene, to_scene)

        rft_frames = [from_scene_rft]

        indices = set(range(to_scene.height * to_scene.width))
        for f in range(to_scene.height * to_scene.width // chars_per_frame + 1):
            rft_frame = rft_frames[f].copy()

            chosen_indices = random.sample(sorted(indices), min(chars_per_frame, len(indices)))
            indices -= set(chosen_indices)
            for i in chosen_indices:
                x, y = i % to_scene.width, i // to_scene.width
                rft_frame[y] = rft_frame[y][:x] + to_scene_rft[y][x] + rft_frame[y][x + 1:]
                fg, bg, tf = to_scene_rft.get_format(y, slice(x, x + 1))[0]
                rft_frame.set_format(y, slice(x, x + 1), fg, bg, tf)
            rft_frames.append(rft_frame)

        del rft_frames[0]
        return ['\n'.join(rft.render()) for rft in rft_frames]

    return inner_scatter

def direct(_: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene is directly shown without any transition.
    :param _: The old scene (discarded)
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    return ['\n'.join(to_scene.get_rendered(suppress_hook=True))]

def get_random(scatter_cpf: int = 100) -> callable:
    """
    Gets a random transition generator function.
    :param scatter_cpf: Number of characters to scatter per frame if scatter transition is chosen.
    """
    return random.choice((
        scatter(scatter_cpf),
        wipe_up_to_down,
        wipe_down_to_up,
        slide_from_top,
        slide_from_bottom,
    ))
