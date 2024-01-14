import pygame
import random

#setup
window_size = 1000
tile_size = 50
tile_range = (tile_size // 2, window_size - tile_size //2, tile_size)

class jeu_snake:

    def __init__(self, taille_fenetre) -> None:
        pygame.init()
        self.fenetre = pygame.display.set_mode([taille_fenetre] * 2)
        self.clock = pygame.time.Clock()
        self.running = True
        self.run(snake(1, 1, pygame.Vector2(self.fenetre.get_width() /2 , self.fenetre.get_height() /2), self.fenetre))

    def run(self, serpent):
        while self.running and serpent.is_alive:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.fenetre.fill("purple")

            # RENDER YOUR GAME HERE
            serpent.move()
            serpent.draw()

            #inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                serpent.direction = 'up'
            elif keys[pygame.K_s]:
                serpent.direction = 'down'
            elif keys[pygame.K_q]:
                serpent.direction = 'left'
            elif keys[pygame.K_d]:
                serpent.direction = 'right'



            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000
        pygame.quit()

class snake:
    direction = 'up'
    time = 0
    is_alive = True
    snake_body = []

    def __init__(self, speed, starting_size, starting_position: pygame.Vector2, screen: pygame.surface) -> None:
        self.speed = speed
        self.size = starting_size
        self.pos = starting_position
        self.screen = screen
        self.new_fruit()

    def grow(self):
        self.size += 1

    def new_fruit(self):
        random_pos = pygame.Vector2(random.randrange(0,self.screen.get_width(),tile_size), random.randrange(0,self.screen.get_height(),tile_size))
        self.fruit = fruit(random_pos , self.screen)

    def draw(self):
        self.snake_rect = pygame.rect.Rect([self.pos, (tile_size -2, tile_size - 2)])
        pygame.draw.rect(self.screen, 'green', self.snake_rect)
        self.fruit.draw()

    def move(self):
        
        #move d'une case toute les 300 ms/speed
        time_now = pygame.time.get_ticks()
        if time_now - self.time > 300/self.speed:
            self.time = time_now
            if self.direction == 'up':
                self.pos.y -= tile_size
            elif self.direction == 'down':
                self.pos.y += tile_size
            elif self.direction == 'left':
                self.pos.x -= tile_size
            elif self.direction == 'right':
                self.pos.x += tile_size

        #meurt si depasse limites ecran
        if (self.pos.y < 0) or (self.pos.y > (self.screen.get_height() - tile_size)) or (self.pos.x < 0) or (self.pos.x > (self.screen.get_height() - tile_size)):
            self.die()

        #verifie si fruit recupéré
        if self.pos == self.fruit.pos :
            self.new_fruit()
            self.grow()

    def die(self):
        print("Game Over")
        self.is_alive = False

class fruit:
    def __init__(self, pos: pygame.Vector2, screen : pygame.surface) -> None:
        self.pos = pos
        self.screen = screen
        self.draw()
    
    def draw(self):
        self.fruit_rect = pygame.rect.Rect([self.pos, (tile_size -2, tile_size - 2)])
        pygame.draw.rect(self.screen, 'yellow', self.fruit_rect)


        

    

jeu_snake(1000)