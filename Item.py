import pygame

class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 40
        self.height = 40
        self.velocity = 5
        if type == 1:
            self.image = pygame.image.load("media/genetic-data.svg")
        elif type == 2:
            self.image = pygame.image.load("media/bacteria-svgrepo-com.svg")
        elif type == 3:
            self.image = pygame.image.load("media/care-day-health-svgrepo-com.svg")
        else:
            self.image = pygame.image.load("media/planet.svg")

        self.rect = self.get_rect()
        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()

    def draw(self, window):
        self.rect = self.get_rect()
        #pygame.draw.rect(window, self.color, self.rect)
        window.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y += self.velocity