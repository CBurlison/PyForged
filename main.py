import pygame
from PythonDI import DIContainer
from InputHandler import *
from pygame.locals import *
from ForgedTypes.tree import Tree
from Helpers import DIHelper
from Scenes.MainMenu.MainMenu import MainMenu

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    FPS = 60
    game_clock = pygame.time.Clock()
    game_clock.tick(FPS)

    di_container = DIContainer()
    di_container.register_instance(DIContainer, di_container)
    di_container.register_instance(pygame.time.Clock, game_clock)

    DIHelper.register_nodes(di_container)

    input_handler = InputHandler()
    di_container.register_instance(InputHandler, input_handler)

    input_handler.add_event(MappedInput(K_RETURN, [KMOD_ALT]), InputTime.JustPressed, handle_input)

    # Set up the drawing window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_tree = Tree(screen)
    di_container.register_instance(Tree, game_tree)

    game_tree.add_child(di_container.locate(MainMenu))

    # Run until the user asks to quit
    running = True
    while running:
        game_clock.tick(FPS)
        frame_ticks = game_clock.get_time()

        delta = 0
        if frame_ticks > 0:
            delta = frame_ticks / 1000.0

        if not input_handler.process_frame_events():
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

if __name__ == "__main__":
    main()