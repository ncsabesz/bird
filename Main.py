'''
Floppy bird game with AI support
'''
import pygame
import neat.config
import neat

import time
import os
import random

from model import Pipe, Bird, Base


class MainApp:
    #set default size for the game windows
    WIN_WIDTH = 550
    WIN_HEIGHT = 800
    FPS = 30

    #score, generation, population counter and set font
    score = 0
    generation = 0
    population = 0

    pygame.font.init()
    START_FONT = pygame.font.SysFont("comicsans",40)

    #set the desired screen size
    #tuple type collection
    screen_size = (WIN_WIDTH,WIN_HEIGHT)

    BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img","bg.png")))

    def __init__(self):
        pass

    #draw the everything on the window screen
    def draw_window(self, win, birds, pipes, base):
        win.blit(self.BG_IMG, (0,0)) #background drawing

        #draw all of the pipes
        for pipe in pipes:
            pipe.draw(win)
        
        #show score
        pipe_passed = self.START_FONT.render("Score: " + str(self.score),1,(255,255,255))
        win.blit(pipe_passed, (5,5))

        #show generation
        generation_counter = self.START_FONT.render("Generation: " + str(self.generation),1,(255,255,255))
        win.blit(generation_counter, (5,45))

        #show population
        genom_counter = self.START_FONT.render("Population: " + str(self.population) + "/" + str(len(birds)),1,(255,255,255))
        win.blit(genom_counter,(5,90))


        base.draw(win)
        for bird in birds:
            bird.draw(win)

        pygame.display.update()
    #end of function draw_window

    #object mover function
    def object_mover(self, win, birds, pipes, base, gen, nets) -> bool:
        trash = [] #this is the pipe trash

        #we have to know wich pipe is in front of us
        #se we can make decision to jump, or not
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            return False


        #check the birds
        for count, bird in enumerate(birds):
            bird.move() #change pos of a bird (down)
            gen[count].fitness += 0.1 #increase a little bit the fitness

            #AI will make decision knowing these data
            data_to_evaluate = ( bird.y,
                                (bird.y - pipes[pipe_ind].height),
                                (bird.y - pipes[pipe_ind].bottom)  
                                )

            #let's make a decision without human interaction
            result = nets[count].activate(data_to_evaluate)

            #result is between 0 and 1 (sigmund activation function)
            if result[0] > 0.5: #if pretty sure...
                bird.jump()
            if result[1] > 0.5: #if pretty sure...
                bird.jumpBig()
        #bird checker loop is over


        #manage the pipes
        for pipe in pipes:
            pipe.move() #change pos of the pipes
            
            #check pipe - bird collision
            for count,bird in enumerate(birds):
                if pipe.collide(bird):
                    gen[count].fitness -= 1 #decrease fitness
                    birds.remove(bird) #delete
                    nets.pop(count) #delete
                    gen.pop(count) #delete

                #birdy left the pipe successfully, so...
                if pipe.passed == False and pipe.x < bird.x:
                    pipe.passed = True
                    self.score += 1 #increase score

                    for g in gen:
                        g.fitness += 5 #increase fitness
                    pipes.append(Pipe(self.WIN_WIDTH+100)) #add another pipe
            #end of birdy loop

    
            #check if pipe left the window
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                trash.append(pipe)
            
            # if pipe.passed == False and pipe.x < bird.x:
            #     pipe.passed = True
            #     score += 1 #increase score
            #     pipes.append(Pipe(WIN_WIDTH+100)) #add another pipe

        #pipemanagement loop is over
        
        #delete the unseen pipes
        for r in trash:
            pipes.remove(r)
        
        #check if any of the birds hit the ground, or fly away
        for count, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                gen[count].fitness -= 1 #decrease fitness
                birds.remove(bird) #delete bird
                nets.pop(count) #delete "brain" (NN)
                gen.pop(count) #delete from generation
        #for loop is over

        base.move()

        #just for fun: above 10 pipes, let's make it faster
        if self.score > 10 and self.FPS < 1000:
            self.FPS += 1
    #end of function object mover

    #this is the main loop, game starts here
    def run_game(self, genomes, config):
        
        #this runs for every new generation
        gen = []
        nets = []
        birds = []
        # global generation
        # global population
        
        # global score
        # global FPS

        self.score = 0
        self.FPS = 30

        self.generation += 1
        self.population = len(genomes)
        
        
        #setup every genomes (g) here
        #genome is a bird in the population
        for ID, g in genomes:
            #we create a brain, a neural network (NN)
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net) #we collect all the NN here in thge list

            birds.append(Bird(random.randrange(100,230), 350)) #we collect birds in the list
            g.fitness = 0 #zero experience
            gen.append(g) #we collect genomes in the list
        #end setup is complete


        pygame.init() #setup the game engine
        pygame.display.set_caption("Programozz Pedroval - 2025")

        base = Base(730) #create the ground object 
        #bird = Bird(230,350) #create the bird object
        pipes = [Pipe(700)] #create an array for the pipes

        win = pygame.display.set_mode(self.screen_size) #create a windows to draw onto
        clock = pygame.time.Clock() #clock handles frame rate

        run = True #game runs until it's true

        #this is the main loop
        while run:
            clock.tick(self.FPS) #FPS is 30

            #check the events, like click
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                    break
                # elif event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_SPACE:
                #          bird.jump()
            #end of events check


            #let's move all of the object
            if self.object_mover(win, birds, pipes, base, gen, nets) == False:
                run = False
                break
            
            #now draw everything
            self.draw_window(win, birds, pipes, base)
        #end of while loop
    #end of function main


    def run(self, config_path):
        try:
            #load the default parameters for natural networks
            config = neat.config.Config(neat.DefaultGenome,
                                        neat.DefaultReproduction,
                                        neat.DefaultSpeciesSet,
                                        neat.DefaultStagnation,
                                        config_path)
        except:
            print("oops, file error, check the file again...")
            return

        #create a population at the beginning
        #the population consists of x genoms (birdies)
        population = neat.Population(config)

        #it executes the main function for 5 times
        #in other words it's 50 generations
        population.run(self.run_game, 50)

        #okay, that's all folks
        pygame.quit()
        quit()
    #end of function run
#end of main class



#the big boom
if __name__ == "__main__":
    #we need an AI config file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    #run the program here
    app = MainApp()
    app.run(config_path)


#end of entry point