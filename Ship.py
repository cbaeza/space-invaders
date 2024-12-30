import pygame

class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.velocity = 10
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = pygame.image.load("media/ship.svg")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, 90)

    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # pygame.draw.rect(ventana,self.color, self.rect)
        window.blit(self.image, (self.x, self.y))