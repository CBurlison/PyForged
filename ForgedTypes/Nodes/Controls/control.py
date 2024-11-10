import sys
sys.path.append("...")

import typing

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

        self.__anchor_point: AnchorPoint = AnchorPoint.TopLeft
        self.__calc_anchor_point = self.__anchor_top_left

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

    @property
    def anchor_point(self) -> AnchorPoint:
        return self.__anchor_point

    @anchor_point.setter
    def anchor_point(self, new_anchor: AnchorPoint):
        self.__anchor_point = new_anchor

        if new_anchor == AnchorPoint.TopLeft:
            self.__calc_anchor_point = self.__anchor_top_left
        elif new_anchor == AnchorPoint.TopCenter:
            self.__calc_anchor_point = self.__anchor_top_center
        elif new_anchor == AnchorPoint.TopRight:
            self.__calc_anchor_point = self.__anchor_top_right
        elif new_anchor == AnchorPoint.LeftCenter:
            self.__calc_anchor_point = self.__anchor_left_center
        elif new_anchor == AnchorPoint.Center:
            self.__calc_anchor_point = self.__anchor_center
        elif new_anchor == AnchorPoint.RightCenter:
            self.__calc_anchor_point = self.__anchor_right_center
        elif new_anchor == AnchorPoint.BottomLeft:
            self.__calc_anchor_point = self.__anchor_bottom_left
        elif new_anchor == AnchorPoint.BottomCenter:
            self.__calc_anchor_point = self.__anchor_bottom_center
        elif new_anchor == AnchorPoint.BottomRight:
            self.__calc_anchor_point = self.__anchor_bottom_right

    def setup(self):
        super().setup()

    def run_mouse_entered_events(self):
        for ev in self.mouse_entered_events:
            ev()

    def run_mouse_exited_events(self):
        for ev in self.mouse_exited_events:
            ev()

    def check_mouse_over(self, pos: tuple[int, int]) -> bool:
        if self.visible and self.mouse_interaction == MouseInterraction.Stop:
            if self.rect is not None and self.rect.collidepoint(pos):
                if not self.mouse_inside:
                    self.mouse_inside = True
                    self.run_mouse_entered_events()
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
        if self.freed:
            return

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
            self.screen.blit(self.surface, self.__calc_anchor_point())

        self.draw_children(self)
        
    def __mouse_exited(self):
        self.mouse_inside = False
        self.run_mouse_exited_events()
        self.mouse_exited()

    ################################################################################################
    #   Anchor methods
    ################################################################################################
    def __anchor_top_left(self) -> tuple[int, int]:
        return self.position

    def __anchor_top_center(self) -> tuple[int, int]:
        adj_x = self.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (adj_x, self.position[1])

    def __anchor_top_right(self) -> tuple[int, int]:
        adj_x = self.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (self.position[0] - self.rect.w, self.position[1])

    def __anchor_left_center(self) -> tuple[int, int]:
        adj_y = self.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)
        return (self.position[0], adj_y)

    def __anchor_center(self) -> tuple[int, int]:
        adj_x = self.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)

        adj_y = self.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)

        return (adj_x, adj_y)

    def __anchor_right_center(self) -> tuple[int, int]:
        adj_y = self.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)

        return (self.position[0] - self.rect.w, adj_y)

    def __anchor_bottom_left(self) -> tuple[int, int]:
        return (self.position[0], self.position[1] - self.rect.h)

    def __anchor_bottom_center(self) -> tuple[int, int]:
        adj_x = self.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (adj_x, self.position[1] - self.rect.h)

    def __anchor_bottom_right(self) -> tuple[int, int]:
        return (self.position[0] - self.rect.w, self.position[1] - self.rect.h)
