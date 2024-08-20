import pygame
from settings import *

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups):
        # loading bird images
        BIRD_IMGS = []
        for i in range(1, 5):
            bird_image_path = os.path.join("..", "..", "..", "imgs", f"bird{i}.png")
            BIRD_IMGS.append(pygame.transform.scale2x(pygame.image.load(bird_image_path)))

        # setting layer above background and init class
        self._layer = 1
        pygame.sprite.Sprite.__init__(self, groups)

        self.frames = BIRD_IMGS
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 5, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # movement properties
        self.gravity = 2000
        self.speed = 0
        self.max_speed = 800
        self.tilt = 0
        self.rotation_velocity = 400
        self.max_rotation = 30

        self.height = self.pos.y # height reference

        self.has_collide = False
    
    def apply_gravity(self, dt):
        """
            Self explanatory name, function that change the y position / speed of the bird due to the gravity
        """

        if self.speed < self.max_speed:
            self.speed += self.gravity * dt
        else:
            self.speed = self.max_speed
        self.pos.y += self.speed * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        """
            Change velocity when the player jump and take the actual position as the height reference for the rotation angle
        """

        self.speed = -600
        self.height = self.pos.y

    def animate(self, dt):
        """
            Change the frame of the bird when time pass and update rotation angle depending on the position of the bird and its actual angle
        """

        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if self.frame_index > 80:
            self.frame_index = 0

        if self.speed * dt < 0 or self.pos.y < self.height + 50: # setting a maximum tilting angle when the bird fall down too far
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else: # update tilting angle
            if self.tilt > -90:
                self.tilt -= self.rotation_velocity * dt

        if self.tilt <= -80:
            self.image = self.frames[1] # setting a fixed frame when the bird is diving
            self.frame_index = 1

    def rotate(self):
        """
            Change the rotation of the bird image depending on the tilting angle
        """

        rotated_bird = pygame.transform.rotozoom(self.image, self.tilt, 1)
        self.image = rotated_bird
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        """
            Updating of the class object -> apply gravity first, do the animation and update the rotation
        """

        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()