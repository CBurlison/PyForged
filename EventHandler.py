import pygame
from enum import Enum
import Helpers.DictHelper as DictHelper
from pygame.locals import (
    QUIT,
    KEYDOWN,
    KEYUP,
    MOUSEMOTION,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP
)
import Helpers.KeyMap as KeyMap
import uuid

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
    
class EventHandler:
    def __init__(self):
        self.__key_events: dict[uuid.UUID, dict[InputTime, list[any]]] = {}
        self.__mouse_motion_events: list[any] = []
        self.__movement_events: list[any] = []
        self.__key_time_cache: dict[uuid.UUID, int] = {}
        self.__input_map: dict[uuid.UUID, MappedInput] = {}
        self.__custom_events: dict[int, list[any]] = {}

        self.mouse_pos: tuple[int, int] = (0, 0)
        self.__movement: tuple[int, int] = None

    def process_frame_events(self) -> bool:
        self.__process_mouse_move()
        self.__process_movement()

        new_events: list[uuid.UUID] = []

        if not self.__parse_all_events(new_events):
            return False

        self.__process_pressed_events(new_events)

        return True

    def add_event(self, input_key: MappedInput, input_time: InputTime, input_event):
        new_id = self.__map_input(input_key)
        DictHelper.insert_2(self.__key_events, 0, new_id, input_time, input_event)

    def remove_event(self, input_key: MappedInput, input_time: InputTime, input_event):
        new_id = self.__map_input(input_key)
        DictHelper.remove_list_2(self.__key_events, new_id, input_time, input_event)

    def add_custom_event(self, event_id: int, custom_event):
        DictHelper.insert(self.__custom_events, 0, event_id, custom_event)

    def remove_custom_event(self, event_id: int, custom_event):
        DictHelper.remove_list(self.__custom_events, event_id, custom_event)

    def add_mouse_motion_event(self, input_event):
        self.__mouse_motion_events.insert(0, input_event)

    def remove_mouse_motion_event(self, input_event):
        if input_event in self.__mouse_motion_events:
            self.__mouse_motion_events.pop(input_event)

    def add_movement_event(self, input_event):
        self.__movement_events.insert(0, input_event)

    def remove_movement_event(self, input_event):
        if input_event in self.__movement_events:
            self.__movement_events.pop(input_event)

    def __process_mouse_move(self):
        new_pos = pygame.mouse.get_pos()

        if not self.mouse_pos == new_pos:
            self.mouse_pos = new_pos
            for ev in self.__mouse_motion_events:
                if ev(new_pos):
                    break

    def __map_input(self, unmapped: MappedInput) -> uuid.UUID:
        for entry in self.__input_map.items():
            if unmapped == entry[1]:
                return entry[0]
                
        new_id = uuid.uuid4()
        self.__input_map[new_id] = unmapped
        return new_id

    def __parse_all_events(self, new_events: list[uuid.UUID]):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type != MOUSEMOTION:
                self.__parse_event(event, new_events)

        return True

    def __parse_event(self, event: pygame.event.Event, new_events: list[uuid.UUID]):
        if event.type > pygame.USEREVENT:
                self.__process_custom_event(event)
        else:
            if event.type == KEYDOWN and event.key in KeyMap.key_map:
                self.__process_keydown_event(event, new_events)
            elif event.type == KEYUP and event.key in KeyMap.key_map:
                self.__process_keyup_event(event)

    def __process_custom_event(self, event: pygame.event.Event):
        if event.type in self.__custom_events:
            for ev in self.__custom_events[event.type]:
                if ev(event):
                    break

    def __process_keydown_event(self, event: pygame.event.Event, new_events: list[uuid.UUID]):
        for reg_key in self.__key_events:
            reg_event = self.__input_map.get(reg_key)

            if reg_event == event:
                count = DictHelper.increment(self.__key_time_cache, reg_key)
                
                if count == 1:
                    new_events.append(reg_event)
                    self.__process_events(reg_key, InputTime.JustPressed)

    def __process_keyup_event(self, event: pygame.event.Event):
        for reg_key in self.__key_events:
            reg_event = self.__input_map.get(reg_key)

            if reg_key in self.__key_time_cache and reg_event.key == event.key:
                if reg_key in self.__key_time_cache:
                    self.__key_time_cache.pop(reg_key)

                self.__process_events(reg_key, InputTime.JustReleased)
    
    def __process_pressed_events(self, new_events: list[uuid.UUID]):
        for cache_key in self.__key_time_cache.keys():
            if cache_key not in new_events:
                _ = DictHelper.increment(self.__key_time_cache, cache_key)
                self.__process_events(cache_key, InputTime.Pressed)

    def __process_events(self, input_key: uuid.UUID, input_time: InputTime):
        if input_key not in self.__key_events:
            return
        
        events_by_time = self.__key_events[input_key]

        if input_time not in events_by_time:
            return
        
        event_list = events_by_time[input_time]

        for ev in event_list:
            if ev():
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
            if ev(movement):
                break
