import pygame
from settings import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        BIRD_IMGS = []
        for i in range(1, 5):
            bird_image_path = os.path.join("..", "..", "imgs", f"bird{i}.png")
            BIRD_IMGS.append(pygame.transform.scale2x(pygame.image.load(bird_image_path).convert_alpha()))

        self.frames = BIRD_IMGS
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 1000
        self.direction = 0

        self.tilt = 0
        self.rotation_velocity = 200
        self.max_rotation = 30

        self.height = self.pos.y
    
    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.direction = -300
        self.height = self.pos.y

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if self.frame_index > 80:
            self.frame_index = 0

        if self.direction * dt < 0 or self.pos.y < self.height + 50: # setting a maximum tilting angle when the bird fall down too far
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else: # update tilting angle
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity * dt

        if self.tilt <= -80:
            self.image = self.frames[1]
            self.frame_index = 1

    def rotate(self):
        rotated_bird = pygame.transform.rotozoom(self.image, self.tilt, 1)
        self.image = rotated_bird

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()





    # def __init__(self, x, y):
    #     BIRD_IMGS = []
    #     for i in range(1, 5):
    #         bird_image_path = os.path.join("..", "..", "imgs", f"bird{i}.png")
    #         BIRD_IMGS.append(pygame.transform.scale2x(pygame.image.load(bird_image_path).convert_alpha()))
    
    #     self.x = x
    #     self.y = y
    #     self.height = self.y
    #     self.tilt_angle = 0

    #     self.max_rot = 30
    #     self.rot_vel = 9
    #     self.vel = 0
        
    #     self.img_count = 0
    #     self.frames = BIRD_IMGS
    #     self.frame_index = self.frames[0]

    #     self.has_collide = False

    # def draw(self, surf):
    #     if not self.has_collide:
    #         # increase self.img_count -> time evolution
    #         # set the index such that the image change each time img count equals the animatime time modulo the number of images
    #         self.img_count += 1
    #         self.img = self.imgs[(self.img_count // self.animation_time) % len(self.imgs)]
    #         if self.img_count == 80:
    #             self.img_count = 0

    #         # setting the image when the bird is falling down
    #         if self.tilt <= -80:
    #             self.img = self.imgs[1]
    #             self.img_count = self.animation_time * 2 # reset the animation time such that the animation reset