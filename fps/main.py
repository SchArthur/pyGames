# Example file showing a circle moving on screen
import pygame
import map
import player
import math
up_angle = pygame.Vector2(0,-1)
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
            self.castRay(self.player.angle)

            self.screen.blit(self.minimap, minimap_coords)
            

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()

    def castRay(self, angle):
        cellsize = self.map.cell_size
        in_cell_x = (self.player.pos.x % cellsize)
        in_cell_y = (self.player.pos.y % cellsize)
        position_in_cell = pygame.Vector2(in_cell_x,in_cell_y)
        for i in range(5):
            point = self.hor_check(angle,position_in_cell, i)
            pygame.draw.circle(self.minimap, 'yellow', point, 2)

    def ver_check(self, angle, pos_in_cell : pygame.Vector2, steps):
        calc_angle = rotateAngle(angle, -90)
        if calc_angle != 0:
            if angle < 180 :
                # DROITE
                x_nearest = self.map.cell_size - pos_in_cell.x
                x_step = self.map.cell_size
            else :
                # GAUCHE
                x_nearest = -pos_in_cell.x
                x_step = -self.map.cell_size
            y_nearest = x_nearest * math.tan(calc_angle * math.pi/180)
            nearest_point = pygame.Vector2(x_nearest, y_nearest)
            pygame.draw.circle(self.minimap, 'yellow', nearest_point + self.player.pos, 2)
            y_step = x_step * math.tan(calc_angle * math.pi/180)
            point = nearest_point
            for i in range(steps):
                point += pygame.Vector2(x_step, y_step)
                pygame.draw.circle(self.minimap, 'yellow', point + self.player.pos, 2)

    def hor_check(self, angle, pos_in_cell : pygame.Vector2, steps):
        calc_angle = rotateAngle(angle, -90)
        if calc_angle != 0:
            if calc_angle < 180 :
                # DOWN
                y_nearest = self.map.cell_size - pos_in_cell.y
                y_step = self.map.cell_size
            else :
                # UP
                y_nearest = -pos_in_cell.y
                y_step = -self.map.cell_size
            x_nearest = y_nearest / math.tan(calc_angle * math.pi/180)
            nearest_point = pygame.Vector2(x_nearest, y_nearest)
            x_step = y_step / math.tan(calc_angle * math.pi/180)
            point = nearest_point
            for i in range(steps):
                point += pygame.Vector2(x_step, y_step)
            return point + self.player.pos
        return self.player.pos.copy()

def rotateAngle(angle, rotation):
    new_angle = angle
    new_angle += rotation
    while new_angle >= 360:
        new_angle -=360
    while new_angle < 0:
        new_angle +=360

    return new_angle


newGame = game()