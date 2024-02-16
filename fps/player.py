import pygame

class newPlayer():
    def __init__(self, pos) -> None:
        self.pos = pygame.Vector2(pos)
        self.direction = pygame.Vector2(0,-1)
        self.angle = 0
        self.speed = 50
        self.turnspeed = 1.5

    def draw(self, surface):
        pygame.draw.circle(surface, 'red', self.pos, 3)
        pygame.draw.line(surface, 'blue', self.pos, self.direction*10 + self.pos)

    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.pos += self.direction * dt * self.speed
        elif keys[pygame.K_s]:
            self.pos -= self.direction * dt * self.speed
        if keys[pygame.K_q]:
            self.direction = self.direction.rotate(-self.turnspeed)
        elif keys[pygame.K_d]:
            self.direction = self.direction.rotate(self.turnspeed)

def fix_angle(angle) -> int:
    new_angle = angle
    while new_angle >= 360:
        new_angle -=360
    while new_angle < 0:
        new_angle +=360

    return new_angle
