import sys
sys.path.append("....")

import typing

from Data.eventHandler import InputTime
from Data.GameData.imageStore import ImageStore
from Data.ForgedTypes.Models.transform import Transform
from Data.ForgedTypes.Nodes.Controls.Sprites.sprite import Sprite

class Button(Sprite):
    def __init__(self, default_img: str, transform: Transform, image_store: ImageStore):
        super().__init__(transform, image_store)
        self.__toggable: bool = False
        self.toggled: bool = False
        self.set_this_frame: bool = False

        self.default_img: str = default_img
        self.hovered_img: str = default_img
        self.clicked_img: str = default_img
        self.toggled_img: str = default_img
        self.toggled_hovered_img: str = default_img

        self.sprite = default_img

        self.pressed_events: list[typing.Any] = []

    def setup(self):
        super().setup()
        self.event_handler.add_mousebutton_event(self, 1, InputTime.JustPressed, self.__on_click)
        self.event_handler.add_mousebutton_event(self, 1, InputTime.Pressed, self.__on_hold)

    @property
    def toggable(self):
        return self.__toggable
    
    @toggable.setter
    def toggable(self, enable: bool):
        self.__toggable = enable

        if not enable:
            self.toggled = False

    def internal_process(self, delta: float):
        super().internal_process(delta)

        if self.set_this_frame:
            return
        
        if self.mouse_inside:
            if self.toggled:
                self.sprite = self.toggled_hovered_img
                self.set_this_frame = False
                return
            
            self.sprite = self.hovered_img
            self.set_this_frame = False
            return
        
        if self.toggled:
            self.sprite = self.toggled_img
            self.set_this_frame = False
            return
        
        self.sprite = self.default_img
        self.set_this_frame = False

    def pressed(self):
        pass

    def __on_click(self):
        self.sprite = self.clicked_img
        self.set_this_frame = True
        self.pressed()

        for ev in self.pressed_events:
            ev(self)

    def __on_hold(self):
        self.sprite = self.clicked_img
        self.set_this_frame = True
