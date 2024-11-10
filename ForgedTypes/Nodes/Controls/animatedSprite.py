import sys
sys.path.append("...")

import typing
import pygame
from enum import Enum
from ForgedTypes.Animation.animation import Animation
from ForgedTypes.Animation.animationFrame import AnimationFrame
from ForgedTypes.Nodes.Controls.control import Control

class SizeMode(Enum):
    Size = 0
    Sprite = 1

class AnimatedSprite(Control):
    def __init__(self, size_mode: SizeMode = SizeMode.Sprite):
        super().__init__()
        self.__frame_time: float = 0.0
        self.__frame_timer: float = 0.0
        self.__playing: bool = False
        self.__current_animation: Animation = None
        self.__current_frame: AnimationFrame = None
        self.__current_animation_length: int = 0

        self.animation_start_events: list[typing.Any] = []
        self.animation_end_events: list[typing.Any] = []
        self.animation_loop_events: list[typing.Any] = []

        self.size_mode: SizeMode = size_mode
        self.frame: int = 0
        self.animation: str = ""
        self.animations: dict[str, Animation] = {}
        self.loop_count: int = 0

    def set_animation(self, animation: str):
        if animation not in self.animations:
            return
        
        self.__current_animation = self.animations[animation]
        self.__current_animation_length = len(self.__current_animation.frames)
        self.set_frame(0)
        self.__frame_time = 1 / self.__current_animation.fps
        self.loop_count = 0

    def play_animation(self, animation: str):
        if animation not in self.animations:
            return
        
        self.set_animation(animation)
        self.__playing = True
        self.__trigger_events(self.animation_start_events, True)

    def play(self):
        if self.animation not in self.animations or self.__current_animation_length == 0:
            return
        
        self.__playing = True

        if self.frame + 1 == self.__current_animation_length:
            self.set_frame(0)
            
        self.__trigger_events(self.animation_start_events, self.frame < 1 and self.__frame_timer < 1)

    def stop(self):
        self.__playing = False
        self.__trigger_events(self.animation_end_events, self.frame + 1 == self.__current_animation_length)

    def set_frame(self, frame: int, reset_timer: bool = True):
        self.frame = frame

        if reset_timer:
            self.__frame_timer = 0.0

        self.__change_frame(frame)

    def process(self, delta: float):
        if not self.__playing or self.__current_animation_length == 0:
            return
        
        super().process(delta)
        self.__frame_timer += delta

        frame_time = self.__frame_time
        
        if self.__current_frame is not None:
            frame_time = frame_time * self.__current_frame.frame_duration

        if self.__frame_timer < frame_time:
            return
        
        self.__frame_timer -= frame_time
        
        if self.frame + 1 == self.__current_animation_length: # check for loop or stop
            if self.__current_animation.loop:
                self.set_frame(0, False)
                self.__trigger_loop_events()
                self.loop_count += 1
                return
            else: # should never hit this but it somehow snuck through
                self.stop()
                self.__frame_timer = 0.0
                self.loop_count = 0
                return
        else: # continue animation
            self.frame += 1

        self.__change_frame(self.frame)

        if self.frame + 1 == self.__current_animation_length and not self.__current_animation.loop:
            self.stop()
            self.__frame_timer = 0.0
            self.loop_count = 0

    def update_surface(self, force: bool = False):
        if self.__current_frame is not None:
            self.surface = self.__current_frame.frame.copy()
        else:
            self.surface = pygame.Surface((1, 1))

        self.set_rect()

        scale_w = self.scale
        scale_h = self.scale

        if self.size_mode == SizeMode.Size:
            if self.rect.w > 0 and self.size[0] > 0:
                scale_w *= (self.size[0] / self.rect.w)
            if self.rect.h > 0 and self.size[1] > 0:
                scale_h *= (self.size[1] / self.rect.h)

        if scale_w != 1.0 or scale_h != 1.0:
            self.surface = pygame.transform.scale(self.surface, (self.rect.w * scale_w, self.rect.h * scale_h))
            self.set_rect()

    def __trigger_loop_events(self):
        for ev in self.animation_loop_events:
            ev(self)

    def __trigger_events(self, events: list[typing.Any], start_end: bool):
        for ev in events:
            ev(self, start_end)

    def __change_frame(self, frame: int):
        self.__current_frame = self.__current_animation.frames[frame]
        self.update_surface(True)
        self.surface.set_colorkey(self.color)