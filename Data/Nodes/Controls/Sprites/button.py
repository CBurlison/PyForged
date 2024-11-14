import typing

from Data.eventHandler import InputTime
from Data.GameData.imageStore import ImageStore
from Data.Models.transform import Transform
from Data.Nodes.Controls.Sprites.sprite import Sprite
from Data.Nodes.Controls.control import MouseInterraction

class Button(Sprite):
    def __init__(self, default_img: str, transform: Transform, image_store: ImageStore):
        super().__init__(transform, image_store)
        self.name = "Button"
        self.__toggable: bool = False
        self.__button_group: str | None = None
        self.__toggled: bool = False
        self.unique_toggle: bool = False
        self.set_this_frame: bool = False

        self.default_img: str = default_img
        self.hovered_img: str = default_img
        self.clicked_img: str = default_img
        self.toggled_img: str = default_img
        self.toggled_hovered_img: str = default_img

        self.sprite = default_img
        self.mouse_interaction = MouseInterraction.Stop

        self.pressed_events: list[typing.Any] = []

    def setup(self):
        super().setup()
        self.event_handler.add_mousebutton_event(self, 1, InputTime.JustPressed, self.__on_click)
        self.event_handler.add_mousebutton_event(self, 1, InputTime.Pressed, self.__on_hold)

    @property
    def toggable(self) -> bool:
        return self.__toggable
    
    @toggable.setter
    def toggable(self, enable: bool):
        self.__toggable = enable

        if not enable:
            self.toggled = False

    @property
    def toggled(self) -> bool:
        return self.__toggled
    
    @toggled.setter
    def toggled(self, enable: bool):
        self.__toggled = enable
        
        if self.toggled and self.unique_toggle:
            btns: list["Button"] = self.event_handler.get_buttons_by_group(self.button_group)
            for btn in btns:
                if btn != self:
                    btn.toggled = False

    @property
    def button_group(self) -> str | None:
        return self.__button_group
    
    @button_group.setter
    def button_group(self, new_group: str | None):
        self.__button_group = new_group
        
        if self.event_handler is not None:
            self.event_handler.clear_button_groups()

    def internal_process(self, delta: float):
        super().internal_process(delta)

        if self.set_this_frame:
            self.set_this_frame = False
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
        if self.toggable:
            self.toggled = not self.toggled

        self.sprite = self.clicked_img
        self.set_this_frame = True
        self.pressed()

        for ev in self.pressed_events:
            ev(self)

    def __on_hold(self):
        self.sprite = self.clicked_img
        self.set_this_frame = True

    def free(self):
        self.event_handler.clear_button_groups()
        super().free()

    def internal_enter_tree(self):
        super().internal_enter_tree()
        self.event_handler.clear_button_groups()

    def internal_exit_tree(self):
        super().internal_exit_tree()
        self.event_handler.clear_button_groups()