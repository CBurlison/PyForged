import pygame
from Data.Models.Animation.animationFrame import AnimationFrame

BLACK: tuple[int, int, int] = (0, 0, 0)

def create_frame(img: pygame.Surface, color: tuple[int, int, int] = BLACK, frame_duration: float = 1.0) -> AnimationFrame:
    rect = img.get_rect()
    width: int = rect.width
    height: int = rect.height

    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(img, (0, 0))
    frame.set_colorkey(color)

    return AnimationFrame(frame, frame_duration)

def create_atlas_surface(img: pygame.Surface, position: tuple[int, int], width: int, height: int, color: tuple[int, int, int] = BLACK) -> pygame.Surface:
    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(img, (0, 0), (position[0], position[1], width, height))
    frame.set_colorkey(color)

    return frame
    
def create_atlas_animation_frame(img: pygame.Surface, position: tuple[int, int], width: int, height: int, color: tuple[int, int, int] = BLACK, frame_duration: float = 1.0) -> AnimationFrame:
    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(img, (0, 0), (position[0], position[1], width, height))
    frame.set_colorkey(color)

    return AnimationFrame(frame, frame_duration)
    
def alter_color(img: pygame.Surface, color: tuple[int, int, int], replace_color: tuple[int, int, int], threshold: tuple[int, int, int] = (0, 0, 0)) -> pygame.Surface:
    target = img.copy()
    pygame.transform.threshold(target, img, color, threshold, replace_color, inverse_set=True)
    return target
