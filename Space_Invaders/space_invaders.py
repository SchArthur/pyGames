# Example file showing a circle moving on screen
import pygame

#colors
bg_color = "#EDDACF"
player_color = "#9F715D"
enemy_color = "#7F513D"

#setting
dev_mode = False
death_line_y = 600

# pygame setup
pygame.init()

class jeu:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_alien_move = 0
        self.running = True
        self.alien_speed = 1
        self.shoot_cd = 300
        self.list_missile = []
        self.last_shoot = 0 - self.shoot_cd
        self.joueur1 = player(self.screen)
        self.createAliens()
        self.run()
        

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.time_now = pygame.time.get_ticks()

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(bg_color)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.joueur1.pos.x -= 300 * self.dt
            elif keys[pygame.K_d]:
                self.joueur1.pos.x += 300 * self.dt
            if keys[pygame.K_ESCAPE]:       
                self.running = False
            if keys[pygame.K_SPACE]:
                self.shoot()

            if keys[pygame.K_TAB]: 
                dev_mode = True
            else:
                dev_mode = False
                
            # dev_mode
            if dev_mode:
                pygame.draw.line(self.screen, 'purple', (0,death_line_y),(self.screen.get_width(),death_line_y), 2)

            # Aliens
            if len(self.list_aliens) > 0:
                if self.time_now - self.last_alien_move > 400/self.alien_speed:
                    self.last_alien_move = self.time_now
                    self.moveAliens()
            
            # Draw
                # aliens
            for elt in self.list_aliens:
                elt.draw()
                # missile
            for elt in self.list_missile:
                elt.draw()
                if elt.pos.y < -100 :
                    self.list_missile.remove(elt)
                for elt_alien in self.list_aliens:
                    if elt_alien.rect_alien.collidepoint(elt.pos.x,elt.pos.y):
                        self.list_aliens.remove(elt_alien)
                        self.list_missile.remove(elt)
                        break
                        
            
            self.joueur1.draw()
            self.stillAlive()
            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def createAliens(self):
        ecart_horizontal = 90
        ecart_vertical = 70
        lignes = 4
        alien_par_colone = 10
        self.list_aliens = []
        vague1 = []
        for y in range(1, lignes+1):
            for x in range(1,alien_par_colone+1):
                vague1.append(pygame.Vector2(ecart_horizontal*x,ecart_vertical*y))
        for elt in vague1:
            self.list_aliens.append(alien(elt, self.screen))

    def shoot(self):
        if self.time_now > self.last_shoot + self.shoot_cd:
            self.last_shoot = self.time_now
            self.list_missile.append(missile(self.screen, pygame.Vector2(self.joueur1.pos.x, self.joueur1.pos.y), self.dt))
                  
    def moveAliens(self):
        threshold_max = self.screen.get_width() - self.list_aliens[0].size*2
        threshold_min = self.list_aliens[0].size
        self.liste_aliens_rect = []
        #move aliens
        for elt in self.list_aliens:
                elt.roam()
                self.liste_aliens_rect.append(elt.rect_alien)
        #check if max
        for elt in self.list_aliens:
            if (elt.pos.x >= threshold_max) and elt.go_right:
                self.aliensToucheBord("droite")
                self.alien_speed += 1
            if (elt.pos.x <= threshold_min) and (not elt.go_right):
                self.aliensToucheBord("gauche")
                self.alien_speed += 1

    def aliensToucheBord(self, cote):
        if cote == "droite":
            for elt in self.list_aliens:
                    elt.pos.y += 20
                    elt.go_right = False
        elif cote == "gauche":
            for elt in self.list_aliens:
                    elt.pos.y += 20
                    elt.go_right = True

    def stillAlive(self):
        if len(self.list_aliens) > 0:
            if self.list_aliens[-1].pos.y + self.list_aliens[-1].size  > death_line_y:
                self.list_aliens = []
                self.joueur1.death()


class player:
    def __init__(self, ecran) -> None:
        self.screen = ecran
        self.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() - 60)

    def draw(self):
        if self.pos.x > self.screen.get_width():
            self.pos.x = self.screen.get_width()
        elif self.pos.x < 0:
            self.pos.x = 0
        pygame.draw.circle(self.screen, player_color, self.pos, 40)

    def death(self):
        self.pos.y = -80

class alien:
    
    go_right = True
    rect_alien = pygame.rect.Rect(0,0,0,0)
    step = 25
    size = 50
    def __init__(self,spawn_position:pygame.Vector2, ecran) -> None:
        self.pos = spawn_position
        self.screen = ecran
        self.texture = pygame.image.load("sprites/alien_medium_1.png").convert_alpha()
        self.is_alive = True

    def roam(self):
        if self.go_right:
            self.pos.x += self.step
        else:
            self.pos.x -= self.step

    def draw(self):
        self.rect_alien = pygame.rect.Rect(self.pos.x, self.pos.y, self.size, self.size)
        self.screen.blit(pygame.transform.scale(self.texture,(self.size,self.size/2)), self.rect_alien)
        # pygame.draw.rect(self.screen, enemy_color, self.rect_alien)

class missile:
    size = 7
    speed = 500
    def __init__(self,screen, shooting_pos, dt) -> None:
        self.detlaTime = dt
        self.screen = screen
        self.pos = shooting_pos

    def draw(self):
        self.pos.y -= self.speed*self.detlaTime
        self.missile_rect = pygame.rect.Rect(self.pos.x,self.pos.y,2,self.size)
        pygame.draw.rect(self.screen, player_color,self.missile_rect)
    
    def __del__(self):
        if self.pos.y > 0:
            print("touché")
        

jeu()