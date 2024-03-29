import pygame
import random

#setup
window_size = 900
tile_size = 50

class jeu_snake:

    def __init__(self, taille_fenetre) -> None:
        pygame.init()
        pygame.mixer.music.load("sounds/snake-music.mp3")
        pygame.mixer.music.play()
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
            self.fenetre.fill('#535353')

            # RENDER YOUR GAME HERE
            if serpent.is_alive != True:
                break
            serpent.draw()
            serpent.move()
            score_obj = gui_text(72, (25, 25), self.fenetre)
            score_obj.draw(str(serpent.score), 'black')

            vitesse_obj = gui_text(38, (25, 135), self.fenetre)
            vitesse_obj.draw("Speed/Vitesse : " + str(round(serpent.speed, 2)) + "x", 'black')

            

            #inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:
                serpent.direction_pressed = 'up'
            elif keys[pygame.K_s]:
                serpent.direction_pressed = 'down'
            elif keys[pygame.K_q]:
                serpent.direction_pressed = 'left'
            elif keys[pygame.K_d]:
                serpent.direction_pressed = 'right'



            # flip() the display to put your work on screen
            pygame.display.flip()

            dt = self.clock.tick(60) / 1000
        pygame.quit()

class snake:
    direction = 'up'
    direction_pressed = 'left'
    time = 0
    score = 0
    is_alive = True
    snake_body = []

    def __init__(self, speed, starting_size, starting_position: pygame.Vector2, screen: pygame.surface) -> None:
        #sounds
        pygame.mixer.init()
        self.snake_eat = pygame.mixer.Sound("sounds/snake-eat.wav")
        self.snake_die = pygame.mixer.Sound("sounds/snake-death.wav")

        self.speed = speed
        self.size = starting_size
        self.pos = starting_position
        self.screen = screen
        self.snake_body.append(pygame.rect.Rect([self.pos, (tile_size -2, tile_size - 2)]))
        self.new_fruit()

    def new_fruit(self):
        random_pos = pygame.Vector2(random.randrange(0,self.screen.get_width(),tile_size), random.randrange(0,self.screen.get_height(),tile_size))
        pos_incorrect = False
        for elt in self.snake_body:
            if pygame.Rect.colliderect(elt, pygame.rect.Rect([random_pos, (tile_size -2, tile_size - 2)])):
                pos_incorrect = True
        
        if pos_incorrect == True:
            self.new_fruit()
        else:
            self.fruit = fruit(random_pos , self.screen)

    def draw(self):
        for elt in self.snake_body:
            pygame.draw.rect(self.screen, 'green', elt)
        self.fruit.draw()
    
    def grow(self):
        self.score += 1
        self.snake_eat.play()
        self.size += 1
        self.speed += 0.1

    def shiftBody(self):
        new_snake_list = []
        new_snake_list.append(pygame.rect.Rect([self.pos, (tile_size -2, tile_size - 2)]))
        for i in range(1, self.size):
            new_snake_list.append(self.snake_body[i-1])
        for i in range(1, self.size):
            if new_snake_list[0] ==  new_snake_list[i]:
                self.die()
        self.snake_body = new_snake_list

    def move(self):
        #move d'une case toute les 300 ms/speed
        time_now = pygame.time.get_ticks()
        if time_now - self.time > 300/self.speed:
            self.time = time_now

            #check si l'inupt est correct
            if self.direction_pressed == 'up':
                if self.direction != 'down':
                    self.direction = 'up'
            elif self.direction_pressed == 'down':
                if self.direction != 'up':
                    self.direction = 'down'
            elif self.direction_pressed == 'left':
                if self.direction != 'right':
                    self.direction = 'left'
            elif self.direction_pressed == 'right':
                if self.direction != 'left':
                    self.direction = 'right'

            #move
            if self.direction == 'up':
                self.pos.y -= tile_size
            elif self.direction == 'down':
                self.pos.y += tile_size
            elif self.direction == 'left':
                self.pos.x -= tile_size
            elif self.direction == 'right':
                self.pos.x += tile_size

            self.shiftBody()

            if (self.pos.y < 0) or (self.pos.y > (self.screen.get_height() - tile_size)) or (self.pos.x < 0) or (self.pos.x > (self.screen.get_height() - tile_size)):
                self.die()
            
            

            #collions
            if pygame.Rect.colliderect(self.snake_body[0], self.fruit.fruit_rect):
                self.new_fruit()
                self.grow()            

    def die(self):
        self.is_alive = False
        channel = self.snake_die.play()
        while channel.get_busy():
            pygame.time.wait(100)
        print("die")

class fruit:
    def __init__(self, pos: pygame.Vector2, screen : pygame.surface) -> None:
        self.pos = pos
        self.screen = screen
        self.draw()
    
    def draw(self):
        self.fruit_rect = pygame.rect.Rect([self.pos, (tile_size -2, tile_size - 2)])
        pygame.draw.rect(self.screen, 'red', self.fruit_rect)

class gui_text:
    font = "impact"
    def __init__(self, size, pos, screen) -> None:
        self.screen = screen
        self.pos = pos
        self.font = pygame.font.SysFont(self.font , size)

    def draw(self, txt, color):
        text_img = self.font.render(txt, True, color)
        self.screen.blit(text_img, self.pos)

jeu_snake(window_size)