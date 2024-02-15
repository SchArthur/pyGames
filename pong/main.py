# Example file showing a circle moving on screen
import pygame
import objects

# settings
paddle_offset = 50

# pygame setup
class game():
    def __init__(self) -> None:
        pass
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.player_left = objects.newPaddle(self.screen, paddle_offset, pygame.K_z, pygame.K_s)
        self.player_right = objects.newPaddle(self.screen, self.screen.get_width() - paddle_offset, pygame.K_UP, pygame.K_DOWN)
        self.player_list = []
        self.player_list.append(self.player_left)
        self.player_list.append(self.player_right)

        self.ball = objects.newBall(self.screen)

        self.run()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("#C0C0C0")

            for player in self.player_list:
                player.update(self.dt)
            self.ball.update(self.dt, self.player_list)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

newGame = game()