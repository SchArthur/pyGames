import pygame
import random

class newBall():
    def __init__(self, screen : pygame.surface.Surface) -> None:
        self.screen = screen
        self.direction = pygame.Vector2(0,0)
        self.size = 12
        self.position = pygame.Vector2(screen.get_width()//2, screen.get_height()//2)
        self.speed = 300

    def update(self, dt):
        self.move(dt)
        self.checkPosInScreen()
        self.draw()
        print(self.position)

    def draw(self):
        pygame.draw.circle(self.screen, 'black', self.position, self.size)

    def move(self, dt):
        if self.direction == pygame.Vector2(0,0):
            self.direction = self.getStartingVelocity()
        
        self.position += self.direction * dt * self.speed

    def getStartingVelocity(self):
        direction = random.choice((-1, 1))
        max_angle = 0.8
        vector_raw = pygame.Vector2(direction, random.uniform(-max_angle,max_angle))
        print(vector_raw)
        vector = vector_raw.normalize()
        return vector
    
    def bounce(self, surfaceVector):
        print('colide')
        self.direction = self.direction.reflect(surfaceVector)
    
    def checkPosInScreen(self):
        if (self.position.x < 0) or (self.position.x > self.screen.get_width()):
            self.bounce(pygame.Vector2(1,0))
        elif (self.position.y < 0) or (self.position.y > self.screen.get_height()):
            self.bounce(pygame.Vector2(0,1))