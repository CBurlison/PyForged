import typing

from Data.eventHandler import InputTime
from Data.Factories.nodeFactory import NodeFactory
from Data.GameData.imageStore import ImageStore
from Data.Models.transform import Transform, SizeMode
from Data.Models.fontInfo import FontInfo
from Data.Nodes.Controls.control import AnchorPoint
from Data.Nodes.Controls.label import Label
from Data.Nodes.Controls.Sprites.sprite import Sprite
from Data.Nodes.Controls.control import MouseInterraction

class Button(Sprite):
    def __init__(self, default_img: str, transform: Transform, image_store: ImageStore, node_factory: NodeFactory):
        super().__init__(transform, image_store)
        self.name = "Button"
        self.label: Label = None
        self.__toggable: bool = False
        self.__button_group: str | None = None
        self.__toggled: bool = False
        self.__text: str | None = None

        self.unique_toggle: bool = False
        self.set_this_frame: bool = False

        self.default_img: str = default_img
        self.hovered_img: str = default_img
        self.clicked_img: str = default_img
        self.toggled_img: str = default_img
        self.toggled_hovered_img: str = default_img

        self.sprite: str = default_img
        self.mouse_interaction = MouseInterraction.Stop

        self.node_factory: NodeFactory = node_factory

        self.pressed_events: list[typing.Any] = []
        self.held_events: list[typing.Any] = []

    def setup(self):
        super().setup()
        self.event_handler.add_mousebutton_event(self, 1, InputTime.JustPressed, self.__on_click)
        self.event_handler.add_mousebutton_event(self, 1, InputTime.Pressed, self.__on_hold)

        self.label = self.node_factory.locate_control(Label, [FontInfo(color=(255, 255, 255), outline=2), self.text])
        self.label.anchor_point = AnchorPoint.Center
        self.add_child(self.label)

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
    def button_group(self) -> str:
        return self.__button_group
    
    @button_group.setter
    def button_group(self, new_group: str):
        self.__button_group = new_group
        
        if self.event_handler is not None:
            self.event_handler.clear_button_groups()

    @property
    def text(self) -> str:
        return self.__text
    
    @text.setter
    def text(self, new_text: str):
        self.__text = new_text
        self.label.text = self.__text

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

        if not self.toggled:
            return

        self.sprite = self.clicked_img
        self.set_this_frame = True
        self.pressed()

        for ev in self.pressed_events:
            ev(self)

        return True

    def __on_hold(self):
        self.sprite = self.clicked_img
        self.set_this_frame = True

        if not self.toggled:
            return
        
        for ev in self.held_events:
            ev(self)

        return True

    def free(self):
        self.event_handler.clear_button_groups()
        super().free()

        self.label = None
        self.__button_group = None
        self.__text = None

        self.default_img = None
        self.hovered_img = None
        self.clicked_img = None
        self.toggled_img = None
        self.toggled_hovered_img = None

        self.node_factory = None

        self.pressed_events.clear()
        self.pressed_events = None

        self.held_events.clear()
        self.held_events = None

    def internal_enter_tree(self):
        super().internal_enter_tree()
        self.event_handler.clear_button_groups()

    def internal_exit_tree(self):
        super().internal_exit_tree()
        self.event_handler.clear_button_groups()

    def set_rect(self):
        super().set_rect()

        if self.label is not None:
            self.label.transform = self.transform.copy()
            self.label.transform.owner = self.label
            self.label.transform.size_mode = SizeMode.Sprite
