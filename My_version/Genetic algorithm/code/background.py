import pygame
from settings import *

class BG(pygame.sprite.Sprite):
    def __init__(self, groups):
        # loading images
        bg_image_path = os.path.join("..", "..", "..", "imgs", "bg.png")
        BG_IMG = pygame.transform.scale2x(pygame.image.load(bg_image_path))

        # setting the layer
        self._layer = 0
        pygame.sprite.Sprite.__init__(self, groups)

        self.image = pygame.Surface((WINDOW_WIDTH * 2, WINDOW_HEIGHT)) # making the surface twice the WINDOW_WIDTH size for smooth and continuous scrolling
        self.image.blit(BG_IMG, (0,0))
        self.image.blit(BG_IMG, (WINDOW_WIDTH,0))
        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # updating position such that the scrolling is smooth and continuous
        self.pos.x -= 50 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)