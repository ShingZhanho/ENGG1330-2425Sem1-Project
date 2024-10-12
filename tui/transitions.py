"""
Contains generators of frames of transitions between two scenes.
"""

from tui import Scene


def __ensure_same_size(from_scene: Scene, to_scene: Scene):
    if from_scene.width != to_scene.width or from_scene.height != to_scene.height:
        raise ValueError('Scenes must be of the same size.')


def __get_rendered_tuple(s1: Scene, s2: Scene) -> tuple[list[str], list[str]]:
    return s1.get_rendered(suppress_hook=True), s2.get_rendered(suppress_hook=True)


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
        frames.append('\n'.join(to_scene_rendered[:i+1] + from_scene_rendered[i+1:]))
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
        frames.append('\n'.join(to_scene_rendered[-(i+1):] + from_scene_rendered[:from_scene.height-i-1]))
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
        frames.append('\n'.join(from_scene_rendered[i+1:] + to_scene_rendered[:i+1]))
    return frames


def direct(_: Scene, to_scene: Scene) -> list[str]:
    """
    Generates frames of a transition where the new scene is directly shown without any transition.
    :param _: The old scene (discarded)
    :param to_scene: The new scene
    :return: all frames of the transition
    """
    return [''.join(to_scene.get_rendered(suppress_hook=True))]