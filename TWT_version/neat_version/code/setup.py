import os
import pygame
import random

pygame.font.init()

# Basic setup
WINDOW_WIDTH = 560
WINDOW_HEIGHT = 800

# Setting application path
application_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(application_path)

# Loading images
BIRD_IMGS = []
for i in range(1, 5):
    bird_image_path = os.path.join("..", "..", "..", "imgs", f"bird{i}.png")
    BIRD_IMGS.append(pygame.transform.scale2x(pygame.image.load(bird_image_path)))

pipe_image_path = os.path.join("..", "..", "..", "imgs", "pipe.png")
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(pipe_image_path))

base_image_path = os.path.join("..", "..", "..", "imgs", "base.png")
BASE_IMG = pygame.transform.scale2x(pygame.image.load(base_image_path))

bg_image_path = os.path.join("..", "..", "..", "imgs", "bg.png")
BG_IMG = pygame.transform.scale2x(pygame.image.load(bg_image_path))

FONT = pygame.font.SysFont("comicsans", 50)