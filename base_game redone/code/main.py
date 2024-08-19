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

    def init_game(self):
        """
            Function that initialize all the element for the game at the start, i.e., the bird, pipes, the base (or ground), the background and the score / best score
        """

        # sprite setup
        self.bg = BG(self.all_sprites)
        self.bird = Bird(self.all_sprites) 
        self.bottom_pipes = [Pipe([self.all_sprites, self.collision_sprites])]
        self.top_pipes = []
        self.top_pipes.append(self.spawn_top_pipes(self.bottom_pipes[-1]))
        self.base = Base([self.all_sprites, self.collision_sprites])

        # adding the sprites to the groups such that they are print in the corresponding layers and characterized as collidable or not
        self.all_sprites.add(self.bg, self.bird, self.bottom_pipes, self.top_pipes, self.base)
        self.collision_sprites.add(self.bottom_pipes, self.top_pipes, self.base)

        # score setup
        self.score = 0
        with open(os.path.join('..', 'score.txt')) as score_file:
            self.best_score = json.load(score_file)


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
    
    def scoring(self):
        """
            Function that evaluate the score of the player and draw it. 
            Delete Pipe objects when they are at the left of the screen.
            Add 1 to the player score when the player pass the pipes and add another set of pipe at the most right of the screen.
        """
        
        for pipe_idx, pipe in enumerate(self.bottom_pipes):
            # delete pipes when they go out of the screen
            if pipe.rect.x + pipe.image.get_width() < 0:
                    self.bottom_pipes.remove(pipe)
                    self.top_pipes.remove(self.top_pipes[pipe_idx])

            # update player score and add new set of pipes when the player pass the pipes
            if not pipe.passed and pipe.rect. x < self.bird.rect. x:
                pipe.passed = True
                self.score += 1
                # update best score if < to actual score
                if self.best_score <= self.score:
                    self.best_score = self.score
                # adding new pipes
                self.bottom_pipes.append(Pipe([self.all_sprites, self.collision_sprites]))
                self.top_pipes.append(self.spawn_top_pipes(self.bottom_pipes[-1]))
                self.all_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])
                self.collision_sprites.add(self.bottom_pipes[-1], self.top_pipes[-1])

        # drawing of the score / best score
        score_text = self.font.render(f"Score: {self.score} | Best: {self.best_score}", True, "black")
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, 30))
        self.display_surface.blit(score_text, score_rect)

    def collision_detection(self):
        """
            Function that check collision between the bird and a sprite in the collision sprite (base or pipes) or with a top boundary outside the screen
        """

        if pygame.sprite.spritecollide(self.bird, self.collision_sprites, False, pygame.sprite.collide_mask) or self.bird.rect.y < - 200:
            self.bird.has_collide = True

    def game_over(self):
        """
            What to do when game over (draw best score and what to do to restart the game)
        """

        bg_image_path = os.path.join("..", "..", "imgs", "bg.png")
        BG_IMG = pygame.transform.scale2x(pygame.image.load(bg_image_path).convert_alpha())

        for sprite in self.all_sprites:
            sprite.kill()

        self.display_surface.fill("black")
        self.display_surface.blit(BG_IMG, (0, 0))

        text = pygame.font.SysFont("comicsans", 80).render("GAME OVER", True, "black")
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
        self.display_surface.blit(text, text_rect)

        text = pygame.font.SysFont("comicsans", 30).render("Press ESCAPE to restart", True, "black")
        text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
        self.display_surface.blit(text, text_rect)

        score_text = self.font.render(f"Best Score: {self.best_score}", True, "black")
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, 30))
        self.display_surface.blit(score_text, score_rect)

    def run(self):
        game_over = False
        self.init_game()

        while True:
            dt = self.clock.tick() / 1000 # setting time step

            if game_over:
                self.game_over()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        pygame.quit()
                        exit()
                if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                    self.init_game()  # initialize variables
                    game_over = False
                pygame.display.update()
            
            else:
                # event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                if pygame.key.get_just_pressed()[pygame.K_SPACE]: # chekcing for jump
                    self.bird.jump()
                
                # game logic
                self.display_surface.fill("black")
                self.all_sprites.draw(self.display_surface)
                self.scoring()
                self.all_sprites.update(dt)
                self.collision_detection()

                if self.bird.has_collide:
                    with open(os.path.join('..', 'score.txt'), 'w') as score_file:
                        json.dump(self.best_score, score_file)
                    game_over = True

                pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()