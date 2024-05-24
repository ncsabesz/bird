import pygame
import os

class Base:
    VEL = 7
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img","base.png")));
    WIDTH = IMG.get_width()
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    #end of function init


    #move 2 ground image together
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #off the screen? Show up on the right
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        #off the screen? Show up on the right
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    #end of function move


    #draw the calculated images
    def draw(self, win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
    #end of function draw

#end of class Base
