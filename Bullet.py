import pygame

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.velocity = 10
        self.color = "white"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("media/bullet.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        #self.image = pygame.transform.rotate(self.image, 180)

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(ventana,self.color, self.rect)
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.y -= self.velocity