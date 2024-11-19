from Data.sceneManager import SceneManager
from Data.Factories.nodeFactory import NodeFactory
from Data.Nodes.Controls.control import Control, AnchorPoint
from Data.Nodes.Controls.Sprites.sprite import Sprite, SizeMode
from Data.Nodes.Controls.Sprites.animatedSprite import AnimatedSprite
from Data.Nodes.Controls.Sprites.button import Button
from Data.Scenes.ToggleButton.toggleButton import ToggleButton

class MainMenu(Control):
    def __init__(self, node_factory: NodeFactory, scene_manager: SceneManager):
        super().__init__()
        self.name = "MainMenu"
        self.speed: int = 100

        self.node_factory: NodeFactory = node_factory
        self.scene_manager: SceneManager = scene_manager
        self.color = (0, 0, 0)

    def setup(self):
        super().setup()
        
        self.update_surface()

        self.transform.size = (self.screen_rect.w, self.screen_rect.h)
        self.transform.position = (0, 0)
        
        anim: AnimatedSprite = self.node_factory.locate_control(AnimatedSprite)
        anim.name = "anim"
        anim.transform.position = (500, 500)
        anim.transform.size_mode = SizeMode.Sprite
        anim.transform.scale = 0.5
        anim.add_animation("idle", "Human_Idle")
        anim.anchor_point = AnchorPoint.TopCenter
        anim.update_surface()
        self.add_child(anim)
        anim.play_animation("idle")
        anim.animation_loop_events.append(self.__loop_10_free)
        anim = None

        anim2: AnimatedSprite = self.node_factory.locate_control(AnimatedSprite)
        anim2.name = "anim2"
        anim2.transform.position = (800, 500)
        anim2.transform.size = (128, 128)
        anim2.transform.size_mode = SizeMode.Size
        anim2.add_animation("idle", "Human_Idle")
        anim2.anchor_point = AnchorPoint.BottomCenter
        anim2.update_surface()
        self.add_child(anim2)
        anim2.play_animation("idle")
        anim2 = None

        sprite: Sprite = self.node_factory.locate_control(Sprite)
        sprite.transform.position = (500, 200)
        sprite.transform.size = (256, 256)
        sprite.sprite = "Human_Portrait"
        sprite.transform.size_mode = SizeMode.Size
        self.add_child(sprite)
        sprite = None

        btn: Button = self.node_factory.locate_control(Button, ["Button"])
        btn.name = "btn"
        btn.text = "Sprite"
        btn.clicked_img = "ButtonPressed"
        btn.hovered_img = "ButtonHovered"
        btn.toggled_img = "ButtonSelected"
        btn.toggled_hovered_img = "ButtonSelectedHovered"
        btn.pressed_events.append(self.__button_pressed)
        btn.transform.size_mode = SizeMode.Sprite
        btn.transform.position = (800, 800)
        self.add_child(btn)
        btn = None
        
        btn2: Button = self.node_factory.locate_control(ToggleButton)
        btn2.name = "btn2"
        btn2.text = "Reload"
        btn2.button_group = "main_menu_toggle_buttons"
        btn2.transform.position = (400, 800)
        btn2.pressed_events.append(self.__reload_button)
        self.add_child(btn2)
        btn2 = None
        
        btn3: Button = self.node_factory.locate_control(ToggleButton)
        btn3.name = "btn3"
        btn3.text = "btn3"
        btn3.button_group = "main_menu_toggle_buttons"
        btn3.transform.position = (600, 800)
        btn3.toggled = True
        self.add_child(btn3)
        btn3 = None
        
        btn4: Button = self.node_factory.locate_control(ToggleButton)
        btn4.name = "btn4"
        btn4.text = "btn4"
        btn4.button_group = "main_menu_toggle_buttons"
        btn4.transform.position = (400, 875)
        self.add_child(btn4)
        btn4 = None
        
        btn5: Button = self.node_factory.locate_control(ToggleButton)
        btn5.name = "btn5"
        btn5.text = "btn5"
        btn5.button_group = "main_menu_toggle_buttons"
        btn5.transform.position = (600, 875)
        self.add_child(btn5)
        btn5 = None
        
        btn6: Button = self.node_factory.locate_control(ToggleButton)
        btn6.name = "btn6"
        btn6.text = "btn6"
        btn6.button_group = "main_menu_toggle_buttons"
        btn6.transform.position = (700, 875)
        self.add_child(btn6)
        btn6 = None
    
    def __loop_10_free(self, anim: AnimatedSprite):
        if anim.loop_count == 2:
            anim.queue_free()

    def __button_pressed(self, btn: Button):
        node = self.get_node("anim2")
        
        if node is not None:
            node.queue_free()

    def __reload_button(self, btn: Button):
        self.scene_manager.change_scene(MainMenu)