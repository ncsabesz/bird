import pygame
import os
import random

class Pipe:
    GAP = 120 #space between the pipes
    VEL = 6 #speed of pipes

    #setup parameters
    def __init__(self, x):
        self.PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img","pipe.png")))

        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0

        #a pipe object contains 2 pipes actually
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG

        self.passed = False #bird passed the pipe?
        self.set_height()
    #end of function __init__


    #set random pipe heights
    def set_height(self):
        self.height = random.randrange(30, 550)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    #end of function set_height


    #move the pipes along x axis
    def move(self):
        self.x -= self.VEL
    #end of function move


    #let's draw the 2 pipes
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    #end of function draw


    #collision checking
    def collide(self, bird):
        #get the mask of the objects to check
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        #check the distance between objects
        top_offset = (self.x - bird.x, self.top - bird.y)
        botton_offset = (self.x - bird.x, self.bottom - bird.y)

        #is there any overlaping between masks?
        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, botton_offset)

        #if so, then bird hits 1 of the pipes
        if t_point or b_point:
            return True

        #otherwise no collision detected
        return False 
    #end of function collide