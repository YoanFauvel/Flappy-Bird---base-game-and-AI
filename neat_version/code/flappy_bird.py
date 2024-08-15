import os
import pygame
import time
import json
import neat

from setup import *
from bird import Bird
from pipe import Pipe
from base import Base

pygame.font.init()

def draw_window(win, birds, pipes, base, score):
    win.blit(BG_IMG, (0,0))
    for bird in birds:
        bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)

    score = FONT.render(f"Score: {score}", True, "black")
    score_rect = score.get_rect(center=(WINDOW_WIDTH / 2, 30))
    win.blit(score, score_rect)

def main(genomes, config):
    pygame.init()
    clock = pygame.time.Clock()
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    nets = []
    ge = []
    birds = []

    pipes = [Pipe(700)]
    base = Base(730)
    score = 0

    speed_modifier = 1

    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(200, 400))
        genome.fitness = 0
        ge.append(genome)

    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
                quit()
        
        draw_window(win, birds, pipes, base, score)

        add_pipe = False
        pipe_idx = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].top_img.get_width():
                pipe_idx = 1
        else:
            run = False
            break

        for bird_idx, bird in enumerate(birds):
            bird.move()
            ge[bird_idx].fitness += 0.1

            output = nets[bird_idx].activate((bird.y, abs(bird.y - pipes[pipe_idx].height), abs(bird.y - pipes[pipe_idx].bottom)))
            if output[0] > 0.5:
                bird.jump()

        for pipe in pipes:
            for bird in birds:
                if pipe.has_collide(bird):
                    bird.has_collide = True
                if not pipe.passed and pipe.x < bird.x:
                    add_pipe = True
                    pipe.passed = True
            if pipe.x + pipe.top_img.get_width() < 0:
                pipes.remove(pipe)
            pipe.move()

        
        if add_pipe:
            score += 1
            speed_modifier = 1 + score / 100
            print(speed_modifier)
            base.vel = 3 * speed_modifier
            print(base.vel)
            pipes.append(Pipe(WINDOW_WIDTH))
            for pipe in pipes:
                pipe.vel = 3 * speed_modifier
                print(pipe.vel)
            for g in ge:
                g.fitness += 5

        for bird_idx, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= base.y or bird.y + bird.img.get_height() <= -300:
                bird.has_collide = True
            if bird.has_collide:
                ge[bird_idx].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.remove(bird)

        base.move()
        pygame.display.update()

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    winner = p.run(main, 10_000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "..", "neat_configuration.txt")
    run(config_path)