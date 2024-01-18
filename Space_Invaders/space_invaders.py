# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()

class jeu:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.last_alien_move = 0
        self.running = True
        self.alien_speed = 0
        self.joueur1 = player(self.screen)
        self.run()
        

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                self.joueur1.pos.x -= 300 * self.dt
            elif keys[pygame.K_d]:
                self.joueur1.pos.x += 300 * self.dt

            # Joueur
            self.joueur1.draw()

            # Aliens
            time_now = pygame.time.get_ticks()
            if time_now - self.last_alien_move > 300/self.alien_speed:
                self.last_alien_move = time_now
                moveAliens()



            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def moveAliens():
        return

class player:
    def __init__(self, ecran) -> None:
        self.screen = ecran
        self.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() - 60)

    def draw(self):
        if self.pos.x > self.screen.get_width():
            self.pos.x = self.screen.get_width()
        elif self.pos.x < 0:
            self.pos.x = 0
        pygame.draw.circle(self.screen, "red", self.pos, 40)

class alien:
    def __init__(self,spawn_position) -> None:
        self.pos = spawn_position
        self.is_alive = True
        self.goRight = True
        self.roam()

    def roam(self):
        if self.goRight:
            return


jeu()
