import sys
sys.path.append("...")

import typing
import pygame

from ForgedTypes.Nodes.node import Node
from eventHandler import EventHandler
from enum import Enum
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

class AnchorPoint(Enum):
    TopLeft = 0
    TopCenter = 1
    TopRight = 2
    LeftCenter = 3
    Center = 4
    RightCenter = 5
    BottomLeft = 6
    BottomCenter = 7
    BottomRight = 8

class Control(Node):
    def __init__(self):
        super().__init__()

        self.anchor_point: AnchorPoint = AnchorPoint.TopLeft

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
            if self.rect is not None and self.rect.collidepoint(pos):
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
    
    def draw(self):
        if self.surface is not None and self.screen is not None:
            self.screen.blit(self.surface, self.__calc_anchor_position())

        self.draw_children(self)
        
    def __mouse_exited(self):
        self.mouse_inside = False
        self.mouse_exited()

    def __calc_anchor_position(self) -> tuple[int, int]:
        if self.anchor_point == AnchorPoint.TopLeft:
            return self.position
        elif self.anchor_point == AnchorPoint.TopCenter:
            adj_x = self.position[0]
            if self.rect.w > 0:
                adj_x -= int(self.rect.w / 2)
            return (adj_x, self.position[1])
        elif self.anchor_point == AnchorPoint.TopRight:
            return (self.position[0] - self.rect.w, self.position[1])
        elif self.anchor_point == AnchorPoint.LeftCenter:
            adj_y = self.position[1]
            if self.rect.h > 0:
                adj_y -= int(self.rect.h / 2)
            return (self.position[0], adj_y)
        elif self.anchor_point == AnchorPoint.Center:
            adj_x = self.position[0]
            if self.rect.w > 0:
                adj_x -= int(self.rect.w / 2)

            adj_y = self.position[1]
            if self.rect.h > 0:
                adj_y -= int(self.rect.h / 2)

            return (adj_x, adj_y)
        elif self.anchor_point == AnchorPoint.RightCenter:
            adj_y = self.position[1]
            if self.rect.h > 0:
                adj_y -= int(self.rect.h / 2)

            return (self.position[0] - self.rect.w, adj_y)
        elif self.anchor_point == AnchorPoint.BottomLeft:
            return (self.position[0], self.position[1] - self.rect.h)
        elif self.anchor_point == AnchorPoint.BottomCenter:
            adj_x = self.position[0]
            if self.rect.w > 0:
                adj_x -= int(self.rect.w / 2)
            return (adj_x, self.position[1] - self.rect.h)
        elif self.anchor_point == AnchorPoint.BottomRight:
            return (self.position[0] - self.rect.w, self.position[1] - self.rect.h)
