import sys
sys.path.append("....")

from Data.ForgedTypes.Nodes.Controls.control import Control, MouseInterraction
from Data.Factories.nodeFactory import NodeFactory
from Data.Scenes.MainMenu.flashyBox import FlashyBox
from Data.ForgedTypes.Nodes.Controls.label import Label
from Data.ForgedTypes.Models.fontInfo import FontInfo
from Data.eventHandler import InputTime

class MainMenu(Control):
    def __init__(self, node_factory: NodeFactory):
        super().__init__()
        self.speed: int = 100

        self.node_factory: NodeFactory = node_factory

        self.transform.size = (50, 50)
        self.transform.position = (250, 250)

        self.color = (0, 0, 0)
        self.delta: float = 0.001

        self.mouse_interaction = MouseInterraction.Stop

    def setup(self):
        super().setup()
        
        self.update_surface()

        box: FlashyBox = self.node_factory.locate_control(FlashyBox)
        box.color = (255, 255, 255)
        box.transform.size = (10, 10)
        box.transform.position = (260, 260)
        box.update_surface()
        self.add_child(box)

        label: Label = self.node_factory.locate_control(Label, [FontInfo(bold=True), "Test label"])
        label.transform.position = (250, 230)
        self.add_child(label)

        self.event_handler.add_movement_event(self, self.__move_event)
        self.event_handler.add_mousebutton_event(self, 1, InputTime.JustPressed, self.__mouse_click_event)

    def process(self, delta: float):
        super().process(delta)
        self.delta = delta

    def mouse_entered(self):
        self.transform.position = (self.transform.position[0] - 20, self.transform.position[1] - 20)
        self.transform.size = (self.transform.size[0] + 40, self.transform.size[1] + 40)
        self.update_surface()

        super().mouse_entered()

    def mouse_exited(self):
        self.transform.position = (self.transform.position[0] + 20, self.transform.position[1] + 20)
        self.transform.size = (self.transform.size[0] - 40, self.transform.size[1] - 40)
        self.update_surface()
        
        super().mouse_exited()

    def __move_event(self, movement: tuple[int, int]):
        move = self.__calc_move()
        calc_move = (int(movement[0] * move), int(movement[1] * move))

        self.move(calc_move)

        return True

    def __calc_move(self) -> float:
        return self.delta * self.speed
    
    def __mouse_click_event(self):
        print("Clicked!")
        return True