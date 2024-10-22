from tui import Scene
import tui.transitions as transitions
import time
import os


class Screen(object):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.__blank_scene = Scene(screen_width, screen_height)
        self.__current_scene = self.__blank_scene
        self.__current_scene.register_scene_update_hook(self.print_scene)
        self.__current_scene.render()


    def transition_into_scene(self, new_scene: Scene, transition: callable = transitions.direct, time_per_frame: float = 0.1):
        """
        Transition into a new scene.
        """
        self.__current_scene.remove_scene_update_hook()
        new_scene.register_scene_update_hook(self.print_scene)
        frames = None
        if self.__current_scene.exit_transition is not None:
            # overrides transition if exit_transition is specified
            frames = self.__current_scene.exit_transition(self.__current_scene, new_scene)
        else:
            frames = transition(self.__current_scene, new_scene)
        if len(frames) == 1:
            time_per_frame = 0
        for frame in frames:
            time.sleep(time_per_frame)
            self.clear_screen()
            print(frame)
        self.__current_scene = new_scene

    def transition_into_blank_scene(self, transition: callable = transitions.direct, time_per_frame: float = 0.1):
        """
        Transition into a blank scene.
        """
        self.transition_into_scene(self.__blank_scene, transition, time_per_frame)

    def print_scene(self, scene: Scene = None):
        """
        Prints the current scene.
        """
        if scene is None:
            scene = self.__current_scene
        self.clear_screen()
        rendered = scene.get_rendered(suppress_hook=False)
        for line in rendered:
            print(line)

    def play_scene(self):
        """
        Executes the play() method of the current scene and returns its output.
        :return: Outputs of the play() method of the current scene.
        """
        return self.__current_scene.play()

    @staticmethod
    def clear_screen():
        """
        Clear the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')