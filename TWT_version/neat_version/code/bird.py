from setup import *

class Bird:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.max_rot = 30
        self.rot_vel = 9
        self.animation_time = 2
        self.imgs = BIRD_IMGS
        
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.imgs[0]

        self.has_collide = False
    
    def jump(self):
        self.vel = -4.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        if not self.has_collide:
            # evaluate the distance travelled by the bird
            self.tick_count += 1
            dist = self.vel * self.tick_count + .3 * self.tick_count**2
            # setting distance limits
            if dist >= 16:
                dist = 16
            if dist < 0:
                dist -= 2
            
            # updating y position with the distance travelled
            self.y += 1/2 * dist

            # evaluate the tilting angle of the bird from its position
            if dist < 0 or self.y < self.height + 50: # setting a maximum tilting angle when the bird fall down too far
                if self.tilt < self.max_rot:
                    self.tilt = self.max_rot
            else: # update tilting angle
                if self.tilt > -90:
                    self.tilt -= self.rot_vel
        else:
            self.tick_count = 0
        
    def draw(self, win):
        if not self.has_collide:
            # increase self.img_count -> time evolution
            # set the index such that the image change each time img count equals the animatime time modulo the number of images
            self.img_count += 1
            self.img = self.imgs[(self.img_count // self.animation_time) % len(self.imgs)]
            if self.img_count == 80:
                self.img_count = 0

            # setting the image when the bird is falling down
            if self.tilt <= -80:
                self.img = self.imgs[1]
                self.img_count = self.animation_time * 2 # reset the animation time such that the animation reset

        # set the rotation of the image arount its center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)