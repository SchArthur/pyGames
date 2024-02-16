# Example file showing a circle moving on screen
import pygame
import map
import player
import math
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
        self.map = map.newMap('map_1.ini', 500)
        self.player = player.newPlayer((11,11))

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

            self.minimap = self.map.drawMiniMap()
            minimap_coords = (0,self.screen.get_height() - self.minimap.get_height())

            self.player.move(self.dt)
            self.player.draw(self.minimap)

            # self.castRay(self.player.direction)
            self.castRay(35)

            self.screen.blit(self.minimap, minimap_coords)
            

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def castRay(self, angle):
        in_cell_x = (self.player.pos.x % self.map.cell_size)
        in_cell_y = (self.player.pos.y % self.map.cell_size)
        position_in_cell = pygame.Vector2(in_cell_x,in_cell_y)
        if (315 <= angle) or (angle < 45) :
            # si HAUT
            print("HAUT")
        elif 45 <= angle < 135:
            # si DROITE
            print("DROITE")
        elif 135 <= angle < 225:
            # si BAS
            print("BAS")
        elif 225 <= angle < 315:
            # si GAUCHE
            print("GAUCHE")

newGame = game()