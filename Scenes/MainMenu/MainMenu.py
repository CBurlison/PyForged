import sys
sys.path.append("...")
sys.path.append("....")

from ForgedTypes.Nodes.Controls.control import Control
from nodeFactory import NodeFactory
from Scenes.MainMenu.flashyBox import FlashyBox
from ForgedTypes.Nodes.Controls.label import Label
from Assets.Fonts.fontInfo import FontInfo
from eventHandler import InputTime
from ForgedTypes.Nodes.Controls.animatedSprite import AnimatedSprite
from Data.animationStore import AnimationStore

class MainMenu(Control):
    def __init__(self, node_factory: NodeFactory, animation_store: AnimationStore):
        super().__init__()
        self.speed: int = 100

        self.node_factory: NodeFactory = node_factory
        self.animation_store: AnimationStore = animation_store

        self.size = (50, 50)
        self.position = (250, 250)
        self.color = (0, 0, 0)
        self.delta: float = 0.001

    def setup(self):
        super().setup()
        
        self.update_surface()

        box: FlashyBox = self.node_factory.locate_control(FlashyBox)
        box.color = (255, 255, 255)
        box.size = (10, 10)
        box.position = (260, 260)
        box.update_surface()

        self.add_child(box)

        label: Label = self.node_factory.locate_control(Label, [FontInfo(bold=True), "Test label"])
        label.position = (250, 230)
        
        label.update_surface()
        self.add_child(label)

        anim: AnimatedSprite = self.node_factory.locate_control(AnimatedSprite)
        anim.position = (500, 500)
        anim.size = (512, 512)
        anim.animations["idle"] = self.animation_store.animations["Human_Idle"]

        anim.update_surface()
        self.add_child(anim)

        anim.play_animation("idle")

        self.event_handler.add_movement_event(self, self.__move_event)
        self.event_handler.add_mousebutton_event(self, 1, InputTime.JustPressed, self.__mouse_click_event)

    def process(self, delta: float):
        super().process(delta)
        self.delta = delta

    def mouse_entered(self):
        self.position = (self.position[0] - 20, self.position[1] - 20)
        self.size = (self.size[0] + 40, self.size[1] + 40)
        self.update_surface()

        super().mouse_entered()

    def mouse_exited(self):
        self.position = (self.position[0] + 20, self.position[1] + 20)
        self.size = (self.size[0] - 40, self.size[1] - 40)
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
