import pygame
import random
from settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, groups):
        # setting layer above background
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, groups)
        
        # loading images
        pipe_image_path = os.path.join("..", "..", "imgs", "pipe.png")
        PIPE_IMG = pygame.transform.scale2x(pygame.image.load(pipe_image_path))

        self.image = PIPE_IMG
        self.rect = self.image.get_rect(topleft=(WINDOW_WIDTH, random.randrange(250, 650)))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        
        # basic properties
        self.passed = False
        self.vel = 250

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        # update position
        self.pos.x -= self.vel * dt
        self.rect.x = round(self.pos.x)