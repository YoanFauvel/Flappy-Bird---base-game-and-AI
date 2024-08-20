import os
import pygame
import time
import json

from settings import *
from bird import Bird
from background import BG
from pipe import Pipe 
from base import Base
from bird_population import Bird_Population


class Game:
    """
        Class for running the flappy bird game
    """

    def __init__(self):
        # basic initialisation
        pygame.init()
        pygame.font.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()

        # setting sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.collision_sprites = pygame.sprite.LayeredUpdates()

        # text
        self.font = pygame.font.SysFont("comicsans", 50)

        self.add_pipe = False

    def spawn_top_pipes(self, bottom_pipe: object) -> object:
        """
            Function that create the corresponding top pipe to the bottom pipe input.

            ...

            Parameter
            ----------
            bottom_pipe : object
                A Pipe object that is oriented from bottom to top

            Return
            ------
            top_pipe : object
                A Pipe object oriented from top to bottom at the same location that the bottom_pipe object shifted in the y direction
        """

        top_pipe = Pipe([self.all_sprites, self.collision_sprites])
        x, y = bottom_pipe.rect.x, bottom_pipe.rect.y
        top_pipe.rect.x, top_pipe.rect.y = x, y - top_pipe.image.get_height() - 200
        top_pipe.image = pygame.transform.rotozoom(top_pipe.image, 180, 1)
        return top_pipe
    
    def scoring(self, bird):
        """
            Function that evaluate the score of the player and draw it. 
            Delete Pipe objects when they are at the left of the screen.
            Add 1 to the player score when the player pass the pipes and add another set of pipe at the most right of the screen.
        """
        
        if not self.bottom_pipes[-1].passed and self.bottom_pipes[-1].rect.x < bird.rect.x:
            self.score += 1
            self.bottom_pipes.append(Pipe([self.all_sprites, self.collision_sprites]))
            self.top_pipes.append(self.spawn_top_pipes(self.bottom_pipes[-1]))
            self.all_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])
            self.collision_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])

    def collision_detection(self, bird):
        """
            Function that check collision between the bird and a sprite in the collision sprite (base or pipes) or with a top boundary outside the screen
        """

        if pygame.sprite.spritecollide(bird, self.collision_sprites, False, pygame.sprite.collide_mask) or bird.rect.y < - 200:
            bird.has_collide = True

    def run(self):
        # sprite setup
        self.bg = BG(self.all_sprites)
        self.birds = Bird_Population(10, self.all_sprites)
        self.bottom_pipes = [Pipe([self.all_sprites, self.collision_sprites])]
        self.top_pipes = []
        self.top_pipes.append(self.spawn_top_pipes(self.bottom_pipes[-1]))
        self.base = Base([self.all_sprites, self.collision_sprites])

        # adding the sprites to the groups such that they are print in the corresponding layers and characterized as collidable or not
        self.all_sprites.add(self.bg, self.bottom_pipes, self.top_pipes, self.base)
        for bird in self.birds.birds:
            self.all_sprites.add(bird)
        self.collision_sprites.add(self.bottom_pipes, self.top_pipes, self.base)

        # score setup
        self.score = 0

        run = True
        while run:
            # print(self.clock.tick())
            dt = self.clock.tick() / 1000 # setting time step
            

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            pipe_idx = 0
            if len(self.birds.birds) > 0:
                if len(self.bottom_pipes) > 1 and self.birds.birds[0].rect.x > self.bottom_pipes[0].rect.x + self.bottom_pipes[0].image.get_width():
                    pipe_idx = 1
            else:
                run = False
                break
            
            # game logic
            self.display_surface.fill("black")
            self.all_sprites.draw(self.display_surface)

            self.add_pipe = False
            for pipe_idx, pipe in enumerate(self.bottom_pipes):
            # delete pipes when they go out of the screen
                if pipe.rect.x + pipe.image.get_width() < 0:
                        self.bottom_pipes.remove(pipe)
                        self.top_pipes.remove(self.top_pipes[pipe_idx])
            # for bird in self.birds.birds:
            #     if not self.bottom_pipes[-1].passed and self.bottom_pipes[-1].rect.x < bird.rect.x:
            #         self.bottom_pipes[-1].passed = True
            #         self.score += 1
            #         self.bottom_pipes.append(Pipe([self.all_sprites, self.collision_sprites]))
            #         self.top_pipes.append(self.spawn_top_pipes(self.bottom_pipes[-1]))
            #         self.all_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])
            #         self.collision_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])

            # drawing of the score / best score
            score_text = self.font.render(f"Score: {self.score}", True, "black")
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, 30))
            self.display_surface.blit(score_text, score_rect)
            for bird in self.birds.birds:
                self.scoring(bird)
                self.collision_detection(bird)
                # if bird.has_collide:
                #     self.birds.birds.remove(bird)
            self.all_sprites.update(dt)

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()