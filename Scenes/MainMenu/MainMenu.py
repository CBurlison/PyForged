import sys
sys.path.append("...")

from ForgedTypes.control import Control
from PythonDI import DIContainer
from Scenes.MainMenu.flashy_box import FlashyBox
from EventHandler import EventHandler

class MainMenu(Control):
    def __init__(self, container: DIContainer, event_handler: EventHandler):
        super().__init__()
        self.speed: int = 100

        self.container: DIContainer = container
        self.event_handler: EventHandler = event_handler

        self.size = (50, 50)
        self.position = (250, 250)
        self.color = (0, 0, 0)
        self.__delta: float = 0.001

    def setup(self):
        self.update_surface()

        box: FlashyBox = self.container.locate(FlashyBox)
        box.color = (255, 255, 255)
        box.size = (10, 10)
        box.position = (260, 260)
        box.update_surface()

        self.add_child(box)

        self.event_handler.add_movement_event(self.__move_event)

    def process(self, delta: float):
        self.__delta = delta

    def exit_tree(self):
        self.event_handler.remove_movement_event(self.__move_event)

    def __move_event(self, movement: tuple[int, int]):
        move = self.__calc_move()
        calc_move = (int(movement[0] * move), int(movement[1] * move))

        self.move(calc_move)

        return True

    def __calc_move(self) -> float:
        return self.__delta * self.speed
