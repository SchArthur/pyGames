import pygame
import random

class newPaddle():
    def __init__(self, screen : pygame.surface.Surface, x_position, up_key, down_key, width = 10, size = 100) -> None:
        self.screen = screen
        self.width = width
        y_position = self.screen.get_height()//2
        self.pixel_size = size
        self.position = pygame.Vector2(x_position, y_position)

        self.up_key = up_key
        self.down_key = down_key

    def update(self, dt):
        self.checkInputs(dt)
        self.draw()

    def draw(self):
        left_top = (self.position.x - (self.width//2), self.position.y - (self.pixel_size//2))
        width_height = (self.width, self.pixel_size)
        self.player_rect = pygame.rect.Rect(left_top, width_height)
        pygame.draw.rect(self.screen, 'black',self.player_rect)

    def checkInputs(self, dt):
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            self.position.y -= 300 * dt
        elif keys[self.down_key]:
            self.position.y += 300 * dt

class newBall():
    def __init__(self, screen : pygame.surface.Surface) -> None:
        self.screen = screen
        self.direction = pygame.Vector2(0,0)
        self.size = 12
        self.position = pygame.Vector2(screen.get_width()//2, screen.get_height()//2)
        self.speed = 300

    def update(self, dt, paddles):
        self.move(dt)
        self.checkPosInScreen()
        self.checkPaddleCollisions(paddles)
        self.draw()

    def checkPaddleCollisions(self, paddles):
        collider_radius = self.size - 3
        left_top = (self.position.x - collider_radius, self.position.y - collider_radius)
        width_height = (collider_radius *2,collider_radius *2)
        collider_rect = pygame.rect.Rect(left_top, width_height)
        for player in paddles:
            if player.player_rect.colliderect(collider_rect):
                print('collide')
                self.bounce(pygame.Vector2(1,0))


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
        self.direction = self.direction.reflect(surfaceVector)
    
    def checkPosInScreen(self):
        if (self.position.x < 0):
            raise Exception('Joueur 2 gagne, fin de partie')
        elif (self.position.x > self.screen.get_width()):
            raise Exception('Joueur 1 gagne ,fin de partie')
        elif (self.position.y - self.size < 0) or (self.position.y + self.size > self.screen.get_height()):
            self.bounce(pygame.Vector2(0,1))