import os
import pygame
import time
import json

from settings import *
from bird import Bird
from background import BG
from pipe import Pipe 
from base import Base


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # sprite setup
        BG(self.all_sprites)
        self.bird = Bird(self.all_sprites)
        Pipe(self.all_sprites)
        Base(self.all_sprites)

    def run(self):
        game_over = False
        while True:
            dt = self.clock.tick() / 1000
            
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                self.bird.jump()
            
            self.display_surface.fill("black")
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()