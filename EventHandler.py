import pygame
import Helpers.DictHelper as DictHelper
import Helpers.KeyMap as KeyMap
import uuid

from enum import Enum
from pygame.locals import (
    QUIT,
    KEYDOWN,
    KEYUP,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
)

class InputTime(Enum):
    JustPressed = 0
    Pressed = 1
    JustReleased = 2

class MappedInput:
    def __init__(self, key: int, mods: list[int] = []):
        self.key = key
        self.mods = mods

    def __eq__(self, other):
        if isinstance(other, MappedInput):
            if self.key != other.key:
                return False
            
            if len(self.mods) != len(other.mods):
                return False
            
            for mod in self.mods:
                if mod not in other.mods:
                    return False
                
            return True
        elif isinstance(other, pygame.event.Event):
            if other.key is None or self.key != other.key:
                return False
            
            for mod in self.mods:
                if not (other.mod & mod):
                    return False
                
            return True
        
        return NotImplemented
    
class MouseClickEvent:
    def __init__(self, control, button: int, input_time: InputTime, click_event):
        self.id: uuid.UUID = uuid.uuid4()
        self.control = control
        self.button = button
        self.input_time = input_time
        self.click_event = click_event
    
class MouseMoveEvent:
    def __init__(self, control, move_event):
        self.id: uuid.UUID = uuid.uuid4()
        self.control = control
        self.move_event = move_event
    
class MovementEvent:
    def __init__(self, control, move_event):
        self.id: uuid.UUID = uuid.uuid4()
        self.control = control
        self.move_event = move_event
    
class CustomEvent:
    def __init__(self, control, event_id: int, custom_event):
        self.id: uuid.UUID = uuid.uuid4()
        self.control = control
        self.event_id = event_id
        self.custom_event = custom_event
    
class KeyPresskEvent:
    def __init__(self, control, input_id: uuid.UUID, input_time: InputTime, press_event):
        self.id: uuid.UUID = uuid.uuid4()
        self.control = control
        self.input_id = input_id
        self.input_time = input_time
        self.press_event = press_event
    
class EventHandler:
    def __init__(self):
        self.__key_events: dict[uuid.UUID, dict[InputTime, list[KeyPresskEvent]]] = {}
        self.__mouse_button_events: dict[int, dict[InputTime, list[MouseClickEvent]]] = {}
        self.__mouse_motion_events: list[MouseMoveEvent] = []
        self.__movement_events: list[MovementEvent] = []
        self.__custom_events: dict[int, list[CustomEvent]] = {}

        self.__key_time_cache: dict[uuid.UUID, int] = {}
        self.__mouse_time_cache: dict[int, int] = {}

        self.__input_map: dict[uuid.UUID, MappedInput] = {}
        
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_movement: tuple[int, int] = None

    # key press events
    def add_key_press_event(self, control, input_key: MappedInput, input_time: InputTime, input_event) -> KeyPresskEvent:
        new_id = self.__map_input(input_key)
        new_event = KeyPresskEvent(control, new_id, input_time, input_event)
        DictHelper.insert_2(self.__key_events, 0, new_id, input_time, new_event)
        control.key_press_event_storage.append(new_event)
        return new_event

    def remove_event(self, input_event: KeyPresskEvent):
        DictHelper.remove_list_2(self.__key_events, input_event.input_id, input_event.input_time, input_event)

    # custom events
    def add_custom_event(self, control, event_id: int, custom_event) -> CustomEvent:
        new_event = CustomEvent(control, event_id, custom_event)
        DictHelper.insert(self.__custom_events, 0, event_id, new_event)
        control.custom_event_storage.append(new_event)
        return new_event

    def remove_custom_event(self, custom_event: CustomEvent):
        DictHelper.remove_list(self.__custom_events, custom_event.event_id, custom_event.custom_event)

    # mouse motion events
    def add_mouse_motion_event(self, control, input_event) -> MouseMoveEvent:
        new_event = MouseMoveEvent(control, input_event)
        self.__mouse_motion_events.insert(0, new_event)
        control.mouse_move_event_storage.append(new_event)
        return new_event

    def remove_mouse_motion_event(self, input_event: MouseMoveEvent):
        if input_event in self.__mouse_motion_events:
            self.__mouse_motion_events.pop(input_event)

    # movement events
    def add_movement_event(self, control, input_event) -> MovementEvent:
        new_event = MovementEvent(control, input_event)
        self.__movement_events.insert(0, new_event)
        control.movement_event_storage.append(new_event)
        return new_event

    def remove_movement_event(self, input_event: MovementEvent):
        if input_event in self.__movement_events:
            self.__movement_events.pop(input_event)

    # mouse button events
    def add_mousebutton_event(self, control, input_key: int, input_time: InputTime, input_event) -> MouseClickEvent:
        new_event = MouseClickEvent(control, input_key, input_time, input_event)
        DictHelper.insert_2(self.__mouse_button_events, 0, input_key, input_time, new_event)
        control.mouse_click_event_storage.append(new_event)
        return new_event

    def remove_mousebutton_event(self, input_key: MouseClickEvent):
        DictHelper.remove_list_2(self.__mouse_button_events, input_key, input_key.input_time, input_key)

    def process_frame_events(self) -> bool:
        self.__process_mouse_move()
        self.__process_movement()

        new_events: list[uuid.UUID] = []
        new_mouse_events: list[int] = []

        if not self.__parse_all_events(new_events, new_mouse_events):
            return False

        self.__process_pressed_events(new_events)
        self.__process_mousebuttonpressed_events(new_mouse_events)

        return True

    def __process_mouse_move(self):
        new_pos = pygame.mouse.get_pos()

        if self.mouse_pos != new_pos:
            self.mouse_movement = (self.mouse_pos[0] - new_pos[0], self.mouse_pos[1] - new_pos[1])
            self.mouse_pos = new_pos
            for ev in self.__mouse_motion_events:
                if ev.move_event(new_pos):
                    break
        else:
            self.mouse_movement = (0, 0)

    def __map_input(self, unmapped: MappedInput) -> uuid.UUID:
        for entry in self.__input_map.items():
            if unmapped == entry[1]:
                return entry[0]
                
        new_id = uuid.uuid4()
        self.__input_map[new_id] = unmapped
        return new_id

    def __parse_all_events(self, new_events: list[uuid.UUID], new_mouse_events: list[int]):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type != MOUSEMOTION:
                self.__parse_event(event, new_events, new_mouse_events)

        return True

    def __parse_event(self, event: pygame.event.Event, new_events: list[uuid.UUID], new_mouse_events: list[int]):
        if event.type > pygame.USEREVENT:
                self.__process_custom_event(event)
        else:
            if event.type == KEYDOWN and event.key in KeyMap.key_map:
                self.__process_keydown_event(event, new_events)
            elif event.type == KEYUP and event.key in KeyMap.key_map:
                self.__process_keyup_event(event)
            if event.type == MOUSEBUTTONDOWN:
                self.__process_mousebuttondown_event(event, new_mouse_events)
            elif event.type == MOUSEBUTTONUP:
                self.__process_mousebuttonup_event(event)

    def __process_custom_event(self, event: pygame.event.Event):
        if event.type in self.__custom_events:
            for ev in self.__custom_events[event.type]:
                if ev.custom_event(event):
                    break

    def __process_keydown_event(self, event: pygame.event.Event, new_events: list[uuid.UUID]):
        for reg_key in self.__key_events:
            reg_event = self.__input_map.get(reg_key)

            if reg_event == event:
                count = DictHelper.increment(self.__key_time_cache, reg_key)
                
                if count == 1:
                    new_events.append(reg_event)
                    self.__process_events(self.__key_events, reg_key, InputTime.JustPressed)

    def __process_keyup_event(self, event: pygame.event.Event):
        for reg_key in self.__key_events:
            reg_event = self.__input_map.get(reg_key)

            if reg_key in self.__key_time_cache and reg_event.key == event.key:
                if reg_key in self.__key_time_cache:
                    self.__key_time_cache.pop(reg_key)

                self.__process_events(self.__key_events, reg_key, InputTime.JustReleased)
    
    def __process_pressed_events(self, new_events: list[uuid.UUID]):
        for cache_key in self.__key_time_cache.keys():
            if cache_key not in new_events:
                _ = DictHelper.increment(self.__key_time_cache, cache_key)
                self.__process_events(self.__key_events, cache_key, InputTime.Pressed)

    def __process_mousebuttondown_event(self, event: pygame.event.Event, new_events: list[int]):
        for reg_key in self.__mouse_button_events:
            if reg_key == event.button:
                count = DictHelper.increment(self.__mouse_time_cache, reg_key)
                
                if count == 1:
                    new_events.append(reg_key)
                    self.__process_mouseclick_events(self.__mouse_button_events, reg_key, InputTime.JustPressed)

    def __process_mousebuttonup_event(self, event: pygame.event.Event):
        for reg_key in self.__mouse_button_events:
            if reg_key in self.__mouse_time_cache and reg_key == event.button:
                if reg_key in self.__mouse_time_cache:
                    self.__mouse_time_cache.pop(reg_key)

                self.__process_mouseclick_events(self.__mouse_button_events, reg_key, InputTime.JustReleased)
    
    def __process_mousebuttonpressed_events(self, new_events: list[int]):
        for cache_key in self.__mouse_time_cache.keys():
            if cache_key not in new_events:
                _ = DictHelper.increment(self.__mouse_time_cache, cache_key)
                self.__process_mouseclick_events(self.__mouse_button_events, cache_key, InputTime.Pressed)

    def __process_events(self, collection: dict[uuid.UUID, dict[InputTime, list[KeyPresskEvent]]], input_key, input_time: InputTime):
        if input_key not in collection:
            return
        
        events_by_time = collection[input_key]

        if input_time not in events_by_time:
            return
        
        event_list = events_by_time[input_time]

        for ev in event_list:
            if ev.press_event():
                break

    def __process_mouseclick_events(self, collection: dict[int, dict[InputTime, list[MouseClickEvent]]], input_key, input_time: InputTime):
        if input_key not in collection:
            return
        
        events_by_time = collection[input_key]

        if input_time not in events_by_time:
            return
        
        event_list = events_by_time[input_time]

        for ev in event_list:
            if ev.control.mouse_inside:
                if ev.click_event():
                    break

    def __process_movement(self):
        if len(self.__movement_events) == 0:
            return

        x: int = 0
        y: int = 0

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            y -= 1
        if pressed_keys[K_DOWN]:
            y += 1
        if pressed_keys[K_LEFT]:
            x -= 1
        if pressed_keys[K_RIGHT]:
            x += 1

        if x == 0 and y == 0:
            return

        movement = (x, y)
        
        for ev in self.__movement_events:
            if ev.move_event(movement):
                break
