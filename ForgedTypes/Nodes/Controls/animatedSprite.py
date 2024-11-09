import sys
sys.path.append("...")

import typing
from ForgedTypes.Animation.animation import Animation
from ForgedTypes.Animation.animationFrame import AnimationFrame
from ForgedTypes.Nodes.Controls.control import Control

class AnimatedSprite(Control):
    def __init__(self):
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

        self.frame: int = 0
        self.animation: str = ""
        self.animations: dict[str, Animation] = {}

        self.color = None

    def set_animation(self, animation: str):
        if animation not in self.animations:
            return
        
        self.__current_animation = self.animations[animation]
        self.__current_animation_length = len(self.__current_animation.frames)
        self.set_frame(0)
        self.__frame_time = 1 / self.__current_animation.fps

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
                return
            else: # should never hit this but it somehow snuck through
                self.stop()
                self.__frame_timer = 0.0
                return
        else: # continue animation
            self.frame += 1

        self.__change_frame(self.frame)

        if self.frame + 1 == self.__current_animation_length and not self.__current_animation.loop:
            self.stop()
            self.__frame_timer = 0.0

    def __trigger_loop_events(self):
        for ev in self.animation_loop_events:
            ev(self.animation)

    def __trigger_events(self, events: list[typing.Any], start_end: bool):
        for ev in events:
            ev(self.animation, start_end)

    def __change_frame(self, frame: int):
        self.__current_frame = self.__current_animation.frames[frame]
        self.update_surface(True)
        self.surface.blit(self.__current_frame.frame, (0, 0))