import os
import pygame
import time
import json

from setup import *
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

def draw_window(win, bird, pipes, base, score, best_score):
    win.blit(BG_IMG, (0,0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    score = FONT.render(f"Score: {score} | Best: {best_score}", True, "black")
    score_rect = score.get_rect(center=(WINDOW_WIDTH / 2, 30))
    win.blit(score, score_rect)

def init_game():
    # global bird, pipes, base, score, best_score
    bird = Bird(200, 200)
    pipes = [Pipe(700)]
    base = Base(730)
    score = 0
    with open(os.path.join('..', 'score.txt')) as score_file:
        best_score = json.load(score_file)
    
    return bird, pipes, base, score, best_score

def main():
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    bird, pipes, base, score, best_score = init_game()

    run = True
    Game_done = False
    while run:
        clock.tick(60)
        if Game_done:
            win.fill((0, 0, 0))
            win.blit(BG_IMG, (0, 0))
            text = pygame.font.SysFont("comicsans", 80).render("GAME OVER", True, "black")
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
            win.blit(text, text_rect)
            text = pygame.font.SysFont("comicsans", 30).render("Press ESCAPE to restart", True, "black")
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
            win.blit(text, text_rect)
            score = FONT.render(f"Best Score: {best_score}", True, "white")
            score_rect = score.get_rect(center=(WINDOW_WIDTH / 2, 30))
            win.blit(score, score_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
            if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                bird, pipes, base, score, best_score = init_game()  # initialize variables
                Game_done = False
                # continue
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False
            
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                bird.jump()
            
            draw_window(win, bird, pipes, base, score, best_score)

            bird.move()
            for pipe in pipes:
                if pipe.has_collide(bird):
                    bird.has_collide = True
                if pipe.x + pipe.top_img.get_width() < 0:
                    pipes.remove(pipe)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
                    if best_score <= score:
                        best_score = score
                    pipes.append(Pipe(700))
                pipe.move()

            if bird.y + bird.img.get_height() >= base.y:
                bird.has_collide = True

            if bird.has_collide:
                with open(os.path.join('..', 'score.txt'), 'w') as score_file:
                    json.dump(best_score, score_file)
                Game_done = True

            if not run:
                with open(os.path.join('..', 'score.txt'), 'w') as score_file:
                    json.dump(best_score, score_file)

            base.move()
            pygame.display.update()
    
    pygame.quit()
    quit()

if __name__ == "__main__":
    main()