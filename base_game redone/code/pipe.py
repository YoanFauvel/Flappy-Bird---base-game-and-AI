import pygame
import random
from settings import *

class Pipe(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        self.height = 0
        self.gap = 200
        self.vel = 250

        self.top = 0
        self.bottom = 0
        
        pipe_image_path = os.path.join("..", "..", "imgs", "pipe.png")
        PIPE_IMG = pygame.transform.scale2x(pygame.image.load(pipe_image_path).convert_alpha())
        self.image = PIPE_IMG
        self.rect = self.image.get_rect(topleft=(WINDOW_WIDTH,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.set_height()
        self.passed = False

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.bottom = self.height + self.gap
        self.rect.y = self.bottom

    def update(self, dt):
        self.pos.x -= self.vel * dt
        self.rect.x = round(self.pos.x)