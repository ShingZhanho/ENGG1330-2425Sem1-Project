from tui import Scene
import time
import os


class Screen(object):
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.__blank_scene = Scene(screen_width, screen_height, ' ')
        self.__current_scene = self.__blank_scene
        self.__current_scene.render()


    def transition_into_scene(self, new_scene: Scene, transition: callable, time_per_frame: float = 0.1):
        """
        Transition into a new scene.
        """
        new_scene.register_scene_update_hook(self.print_scene)
        frames = transition(self.__current_scene, new_scene)
        if len(frames) == 1:
            time_per_frame = 0
        for frame in frames:
            time.sleep(time_per_frame)
            self.clear_screen()
            print(frame)
        self.__current_scene = new_scene
        self.print_scene()


    def print_scene(self, scene: Scene = None):
        """
        Prints the current scene.
        """
        if scene is None:
            scene = self.__current_scene
        self.clear_screen()
        for y in range(scene.height):
            for x in range(scene.width):
                print(scene.draw(x, y), end='')
            print()


    @staticmethod
    def clear_screen():
        """
        Clear the screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')