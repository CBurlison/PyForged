import pygame
from PythonDI import DIContainer
from EventHandler import EventHandler, MappedInput, InputTime
from pygame.locals import K_RETURN, KMOD_ALT
from ForgedTypes.tree import Tree
from ForgedTypes.game_data import GameData
from Helpers import DIHelper
from Scenes.MainMenu.MainMenu import MainMenu

def main():
    pygame.init()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    FPS = 60
    game_clock = pygame.time.Clock()
    game_clock.tick(FPS)

    di_container = DIContainer()
    di_container.register_instance(DIContainer, di_container)
    di_container.register_instance(pygame.time.Clock, game_clock)
    di_container.register_instance(GameData)

    DIHelper.register_nodes(di_container)

    event_handler = EventHandler()
    di_container.register_instance(EventHandler, event_handler)

    event_handler.add_event(MappedInput(K_RETURN, [KMOD_ALT]), InputTime.JustPressed, handle_input)
    event_handler.add_mouse_motion_event(mouse_moved)

    # Set up the drawing window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    di_container.register_instance(pygame.Surface, screen)
    
    game_tree = Tree(screen)
    di_container.register_instance(Tree, game_tree)

    # Final step before starting game loop
    game_tree.add_child(di_container.locate(MainMenu))

    # Run until the user asks to quit
    while True:
        game_clock.tick(FPS)
        frame_ticks = game_clock.get_time()

        delta = 0
        if frame_ticks > 0:
            delta = frame_ticks / 1000.0

        if not event_handler.process_frame_events():
            break
       
        # Fill the background with white
        game_tree.screen.fill((128, 128, 128))
        
        game_tree.process(delta)

        # Flip the display
        pygame.display.flip()


    # Done! Time to quit.
    pygame.quit()

def handle_input() -> bool:
    print("Input handled!")
    return True

def mouse_moved(pos):
    print(f"New pos {pos}")
    return True

if __name__ == "__main__":
    main()