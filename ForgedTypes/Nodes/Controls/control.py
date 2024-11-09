import sys
sys.path.append("...")

from ForgedTypes.Nodes.node import Node
from eventHandler import EventHandler
from enum import Enum
import typing
from eventHandler import (
    MouseClickEvent,
    MouseMoveEvent,
    KeyPresskEvent,
    MovementEvent,
    CustomEvent
)
class MouseInterraction(Enum):
    Stop = 0
    Ignore = 1

class Control(Node):
    def __init__(self):
        super().__init__()

        self.mouse_entered_events: list[typing.Any] = []
        self.mouse_exited_events: list[typing.Any] = []

        self.mouse_click_event_storage: list[MouseClickEvent] = []
        self.mouse_move_event_storage: list[MouseMoveEvent] = []
        self.movement_event_storage: list[MovementEvent] = []
        self.key_press_event_storage: list[KeyPresskEvent] = []
        self.custom_event_storage: list[CustomEvent] = []

        self.event_handler: EventHandler
        self.mouse_interaction: MouseInterraction = MouseInterraction.Stop
        self.mouse_inside: bool = False

    def setup(self):
        super().setup()

    def mouse_entered(self):
        for ev in self.mouse_entered_events:
            ev()

    def mouse_exited(self):
        for ev in self.mouse_exited_events:
            ev()

    def check_mouse_over(self, pos: tuple[int, int]) -> bool:
        if self.visible and self.mouse_interaction == MouseInterraction.Stop:
            if self.surface_rect is not None and self.surface_rect.collidepoint(pos):
                if not self.mouse_inside:
                    self.mouse_inside = True
                    self.mouse_entered()

                return True

            elif self.mouse_inside:
                self.__mouse_exited()
        else:
            if self.mouse_inside:
                self.__mouse_exited()
            
            for child in self.children:
                if child.check_mouse_over(pos):
                    return True
                
        return False
    
    def free(self):
        for ev in self.mouse_click_event_storage:
            self.event_handler.remove_mousebutton_event(ev)

        for ev in self.custom_event_storage:
            self.event_handler.remove_custom_event(ev)

        for ev in self.movement_event_storage:
            self.event_handler.remove_movement_event(ev)

        for ev in self.key_press_event_storage:
            self.event_handler.remove_event(ev)

        for ev in self.mouse_move_event_storage:
            self.event_handler.remove_mouse_motion_event(ev)

        super().free()
    
    def __mouse_exited(self):
        self.mouse_inside = False
        self.mouse_exited()