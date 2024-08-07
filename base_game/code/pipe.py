from setup import *

class Pipe:
    
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 200
        self.vel = 3

        self.top = 0
        self.bottom = 0
        self.bottom_img = PIPE_IMG
        self.top_img = pygame.transform.flip(PIPE_IMG, False, True)

        self.set_height()
        self.passed = False

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.top_img.get_height()
        self.bottom = self.height + self.gap
    
    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.top_img, (self.x, self.top))
        win.blit(self.bottom_img, (self.x, self.bottom))

    def has_collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_img)
        bottom_mask = pygame.mask.from_surface(self.bottom_img)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset  = (self.x - bird.x, self.bottom - round(bird.y))

        top_collision = bird_mask.overlap(bottom_mask, top_offset)
        bottom_collision = bird_mask.overlap(top_mask, bottom_offset)

        has_collide = top_collision or bottom_collision

        return has_collide