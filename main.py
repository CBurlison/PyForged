import pygame
from PythonDI import DIContainer
from eventHandler import EventHandler
from ForgedTypes.Nodes.tree import Tree
from ForgedTypes.gameState import GameState
from Helpers import DIHelper
from Scenes.MainMenu.mainMenu import MainMenu
from Scenes.FpsCounter.fpsCounter import FpsCounter
from Factories.nodeFactory import NodeFactory
from Data.imageStore import ImageStore
from Data.animationStore import AnimationStore
from ForgedTypes.Nodes.Controls.Sprites.animatedSprite import AnimatedSprite
from ForgedTypes.Nodes.Controls.Sprites.sprite import Sprite, SizeMode
from ForgedTypes.Nodes.Controls.control import AnchorPoint

def loop_10_free(anim: AnimatedSprite):
    if anim.loop_count == 2:
        anim.queue_free()

def main():
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    
    game_clock = pygame.time.Clock()
    game_clock.tick(60)
    
    di_container = DIContainer()
    di_container.register_instance(DIContainer, di_container)

    di_container.register_instance(NodeFactory)
    node_factory: NodeFactory = di_container.locate(NodeFactory)

    di_container.register_instance(pygame.time.Clock, game_clock)
    di_container.register_instance(GameState)

    DIHelper.register_nodes(di_container)

    event_handler = EventHandler()
    di_container.register_instance(EventHandler, event_handler)

    # Set up the drawing window
    di_container.register_instance(pygame.Surface, pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
    di_container.register_instance(ImageStore, ImageStore())
    di_container.register_instance(AnimationStore)
    _ = di_container.locate(AnimationStore)
    
    game_tree = node_factory.locate_node(Tree)
    di_container.register_instance(Tree, game_tree)

    # Final step before starting game loop
    game_tree.add_child(node_factory.locate_control(MainMenu))
    game_data: GameState = di_container.locate(GameState)

    anim: AnimatedSprite = node_factory.locate_control(AnimatedSprite)
    anim.transform.position = (500, 500)
    anim.transform.size_mode = SizeMode.Sprite
    anim.transform.scale = 0.5
    anim.add_animation("idle", "Human_Idle")
    anim.anchor_point = AnchorPoint.TopCenter
    anim.update_surface()
    game_tree.add_child(anim)
    anim.play_animation("idle")
    anim.animation_loop_events.append(loop_10_free)
    anim = None

    anim2: AnimatedSprite = node_factory.locate_control(AnimatedSprite)
    anim2.transform.position = (800, 500)
    anim2.transform.size = (128, 128)
    anim2.transform.size_mode = SizeMode.Size
    anim2.add_animation("idle", "Human_Idle")
    anim2.anchor_point = AnchorPoint.BottomCenter
    anim2.update_surface()
    game_tree.add_child(anim2)
    anim2.play_animation("idle")
    anim2 = None

    sprite: Sprite = node_factory.locate_control(Sprite)
    sprite.transform.position = (500, 200)
    sprite.transform.size = (256, 256)
    sprite.sprite = "Human_Portrait"
    sprite.transform.size_mode = SizeMode.Size
    game_tree.add_child(sprite)
    sprite = None

    fps_label: FpsCounter = node_factory.locate_control(FpsCounter)
    fps_label.position = (SCREEN_WIDTH/2, 60)
    fps_label.size = (SCREEN_WIDTH, 60)
    
    fps_label.update_surface()
    game_tree.add_child(fps_label)
    
    game_tree.screen.fill((128, 128, 128))
    pygame.display.flip()
    game_clock.tick(game_data.FPS)

    node_factory = None

    # Main game loop
    while True:
        frame_ticks = game_clock.get_time()

        delta = 0
        if frame_ticks > 0:
            delta = frame_ticks / 1000.0

        game_data.delta = delta
        game_tree.screen.fill((128, 128, 128))

        if not event_handler.process_frame_events():
            break
       
        game_tree.process_children(game_tree, delta)
        game_tree.check_mouse_over(event_handler.mouse_pos)

        game_tree.run_queue_events()

        game_tree.draw()

        # Flip the display
        pygame.display.update()
        game_clock.tick(game_data.FPS)


    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()