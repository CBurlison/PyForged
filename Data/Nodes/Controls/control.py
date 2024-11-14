import pygame
import typing

from Data.Nodes.node import Node
from Data.Models.inputState import InputState
from enum import Enum
from Data.eventHandler import (
    EventHandler,
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
        self.name = "Control"

        self.__anchor_point: AnchorPoint = AnchorPoint.TopLeft
        self.calc_anchor_point = self.__anchor_top_left
        self.calc_anchor_point_rect = self.__anchor_top_left_rect

        self.mouse_entered_events: list[typing.Any] = []
        self.mouse_exited_events: list[typing.Any] = []

        self.mouse_click_event_storage: list[MouseClickEvent] = []
        self.mouse_move_event_storage: list[MouseMoveEvent] = []
        self.movement_event_storage: list[MovementEvent] = []
        self.key_press_event_storage: list[KeyPresskEvent] = []
        self.custom_event_storage: list[CustomEvent] = []

        self.mouse_interaction: MouseInterraction = MouseInterraction.Ignore
        self.mouse_inside: bool = False
        
        ################################################################################################
        #   set in Factory
        ################################################################################################
        self.event_handler: EventHandler

    @property
    def anchor_point(self) -> AnchorPoint:
        return self.__anchor_point

    @anchor_point.setter
    def anchor_point(self, new_anchor: AnchorPoint):
        self.__anchor_point = new_anchor

        if new_anchor == AnchorPoint.TopLeft:
            self.calc_anchor_point = self.__anchor_top_left
            self.calc_anchor_point_rect = self.__anchor_top_left_rect
        elif new_anchor == AnchorPoint.TopCenter:
            self.calc_anchor_point = self.__anchor_top_center
            self.calc_anchor_point_rect = self.__anchor_top_center_rect
        elif new_anchor == AnchorPoint.TopRight:
            self.calc_anchor_point = self.__anchor_top_right
            self.calc_anchor_point_rect = self.__anchor_top_right_rect
        elif new_anchor == AnchorPoint.LeftCenter:
            self.calc_anchor_point = self.__anchor_left_center
            self.calc_anchor_point_rect = self.__anchor_left_center_rect
        elif new_anchor == AnchorPoint.Center:
            self.calc_anchor_point = self.__anchor_center
            self.calc_anchor_point_rect = self.__anchor_center_rect
        elif new_anchor == AnchorPoint.RightCenter:
            self.calc_anchor_point = self.__anchor_right_center
            self.calc_anchor_point_rect = self.__anchor_right_center_rect
        elif new_anchor == AnchorPoint.BottomLeft:
            self.calc_anchor_point = self.__anchor_bottom_left
            self.calc_anchor_point_rect = self.__anchor_bottom_left_rect
        elif new_anchor == AnchorPoint.BottomCenter:
            self.calc_anchor_point = self.__anchor_bottom_center
            self.calc_anchor_point_rect = self.__anchor_bottom_center_rect
        elif new_anchor == AnchorPoint.BottomRight:
            self.calc_anchor_point = self.__anchor_bottom_right
            self.calc_anchor_point_rect = self.__anchor_bottom_right_rect

    def setup(self):
        super().setup()

    def run_mouse_entered_events(self):
        for ev in self.mouse_entered_events:
            ev()

    def run_mouse_exited_events(self):
        for ev in self.mouse_exited_events:
            ev()

    def check_mouse_over(self, pos: tuple[int, int], state: InputState):
        if not self.visible or self.freed:
            return

        index = len(self.children) - 1
        while index >= 0:
            self.children[index].check_mouse_over(pos, state)
            index -= 1
            
        if self.mouse_interaction == MouseInterraction.Stop:
            #if self.rect is not None and self.calc_anchor_point_rect().collidepoint(pos):
            if not state.handled:
                if self.rect is not None and self.rect.collidepoint(pos):
                    state.handled = True
                    
                    if not self.mouse_inside:
                        self.mouse_inside = True
                        self.run_mouse_entered_events()
                        self.mouse_entered()
                        return
                elif self.mouse_inside:
                    self.__mouse_exited()
                    return
            elif self.mouse_inside:
                self.__mouse_exited()
                return
        else:
            if self.mouse_inside:
                self.__mouse_exited()
    
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
            #self.screen.blit(self.surface, self.calc_anchor_point())
            self.screen.blit(self.surface, self.transform.position)

        self.draw_children(self)
        
    def __mouse_exited(self):
        self.mouse_inside = False
        self.run_mouse_exited_events()
        self.mouse_exited()

    ################################################################################################
    #   Anchor methods
    ################################################################################################
    def __anchor_top_left(self) -> tuple[int, int]:
        return self.transform.position

    def __anchor_top_center(self) -> tuple[int, int]:
        adj_x = self.transform.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (adj_x, self.transform.position[1])

    def __anchor_top_right(self) -> tuple[int, int]:
        adj_x = self.transform.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (self.transform.position[0] - self.rect.w, self.transform.position[1])

    def __anchor_left_center(self) -> tuple[int, int]:
        adj_y = self.transform.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)
        return (self.transform.position[0], adj_y)

    def __anchor_center(self) -> tuple[int, int]:
        adj_x = self.transform.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)

        adj_y = self.transform.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)

        return (adj_x, adj_y)

    def __anchor_right_center(self) -> tuple[int, int]:
        adj_y = self.transform.position[1]
        if self.rect.h > 0:
            adj_y -= int(self.rect.h / 2)

        return (self.transform.position[0] - self.rect.w, adj_y)

    def __anchor_bottom_left(self) -> tuple[int, int]:
        return (self.transform.position[0], self.transform.position[1] - self.rect.h)

    def __anchor_bottom_center(self) -> tuple[int, int]:
        adj_x = self.transform.position[0]
        if self.rect.w > 0:
            adj_x -= int(self.rect.w / 2)
        return (adj_x, self.transform.position[1] - self.rect.h)

    def __anchor_bottom_right(self) -> tuple[int, int]:
        return (self.transform.position[0] - self.rect.w, self.transform.position[1] - self.rect.h)

    ################################################################################################
    #   Anchor Rect methods
    ################################################################################################
    def __anchor_top_left_rect(self) -> pygame.Rect:
        return self.rect

    def __anchor_top_center_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_top_center()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect


    def __anchor_top_right_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_top_right()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_left_center_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_left_center()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_center_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_center()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_right_center_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_right_center()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_bottom_left_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_bottom_left()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_bottom_center_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_bottom_center()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect

    def __anchor_bottom_right_rect(self) -> pygame.Rect:
        rect = self.rect.copy()
        pos = self.__anchor_bottom_right()
        rect.x = pos[0]
        rect.y = pos[1]
        return rect
