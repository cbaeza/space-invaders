import pygame

class Enemy:
    def __init__(self, id, x, y, type):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.width = 50
        self.height = 50
        self.velocity = 5
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.live = 3
        if type == 1:
            self.image = pygame.image.load("media/alien-monster.svg")
        else:
            self.image = pygame.image.load("media/monster-svgrepo-com.svg")

        self.image = pygame.transform.scale(self.image, (self.width, self.height)).convert_alpha()
        
    def draw(self, window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(window,self.color, self.rect)
        window.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.velocity

    def __repr__(self):
        return f"( id: {self.id}, x: {self.x}, y: {self.y}, type: {self.type} )"