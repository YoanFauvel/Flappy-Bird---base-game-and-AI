import pygame
from settings import *

class Base(pygame.sprite.Sprite):
    def __init__(self, groups):
        # super().__init__(groups)
        self._layer = 2
        pygame.sprite.Sprite.__init__(self, groups)
        base_image_path = os.path.join("..", "..", "imgs", "base.png")
        BASE_IMG = pygame.transform.scale2x(pygame.image.load(base_image_path))
        self.image = pygame.Surface((BASE_IMG.get_width() * 2, BASE_IMG.get_height()))
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT + 150))
        self.image.blit(BASE_IMG, (0,0))
        self.image.blit(BASE_IMG, (BASE_IMG.get_width(),0))

        # self.mask = pygame.mask.from_surface(self.image)
        
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 250 * dt 
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)