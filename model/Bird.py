import pygame
import os

class Bird:
    ANIMATION_TIME = 3 #wait time beatween bird animation

    #every class must have a constructor
    def __init__(self, x, y):
        self.BIRD_IMGS = [
            pygame.transform.scale2x(pygame.image.load(os.path.join("img","bird1.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img","bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("img","bird3.png")))
        ]

        self.x = x #x coord of the bird
        self.y = y #y coord of the bird
        self.tick_count = 0 #movment counter
        self.vel = 0 #speed (velocity)
        self.height = self.y
        self.img_count = 0 #image counter for wing animation

        self.img = self.BIRD_IMGS[0]
    #end of function __init__


    #this does the jumping of the bird
    #it means the AI make decision, if jump is necessary
    def jump(self):
        self.vel = -7
        self.tick_count = 0
        self.height = self.y

    def jumpBig(self):
        self.vel = -14
        self.tick_count = 0
        self.height = self.y
    #end of function jump
    

    #lets move the bird
    #it means the birdy keeps falling
    def move(self):
        self.tick_count += 1

        delta = self.vel * self.tick_count + 1.5 * self.tick_count**2

        if delta >= 16:
            delta = 16
        if delta < 0:
            delta += 2

        #let's change the y position of the bird
        self.y = self.y + delta
    #end of function move    


    #draw the bird on the screen
    def draw(self, win):
        self.img_count += 1

        #slow down the flapping of the wings
        if self.img_count == self.ANIMATION_TIME:
            self.img = self.BIRD_IMGS[0]
        if self.img_count == (self.ANIMATION_TIME * 2):
            self.img = self.BIRD_IMGS[1]
        if self.img_count == (self.ANIMATION_TIME * 3):
            self.img = self.BIRD_IMGS[2]
            self.img_count = 0

        #copy the image to windows screen
        win.blit(self.img,(self.x, self.y))
    #end of function draw


    #get a mask for collision detection
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    #end of funczion get_mask