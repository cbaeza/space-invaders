import datetime
from time import sleep

import pygame
from Ship import Ship
from Enemy import Enemy
from Bullet import Bullet
from Item import Item
import random

class SpaceInvaders:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.enemy_count = 0
        self.last_item = 0
        self.last_bullet = 0
        self.WINDOWS_WIDTH = 1134
        self.WINDOWS_HEIGHT = 765
        self.WINDOW = pygame.display.set_mode([self.WINDOWS_WIDTH, self.WINDOWS_HEIGHT])
        self.FRAME_PER_SECONDS = 60
        self.FRONT = pygame.font.SysFont("Comic Sans", 40)
        self.SOUND_SHOT = pygame.mixer.Sound('media/laser.mp3')
        self.SOUND_GAME_OVER = pygame.mixer.Sound('media/game-over.mp3')
        self.SOUND_DEATH = pygame.mixer.Sound('media/laser-loop-tail.mp3')
        self.BACKGROUND = pygame.image.load("media/space.png").convert_alpha()

        self.playing = True
        self.clock = pygame.time.Clock()

        self.life = 5
        self.score = 0

        self.pass_time = 0
        self.time_between_enemies = 500 # ms

        self.ship = Ship(self.WINDOWS_WIDTH / 2, self.WINDOWS_HEIGHT - 75)

        self.enemies = []
        self.bullets = []
        self.items = []

        self.last_bullet = 0
        self.time_between_bullets = 50 # ms

        self.last_item = 0
        self.time_between_items = 3000 # ms

        self.enemies.append(self.create_enemy())

    def create_bullet(self):
            if pygame.time.get_ticks() - self.last_bullet > self.time_between_bullets:
                self.bullets.append(Bullet(self.ship.rect.centerx, self.ship.rect.centery))
                self.last_bullet = pygame.time.get_ticks()
                self.SOUND_SHOT.play()

    def create_item(self):
            if pygame.time.get_ticks() - self.last_item > self.time_between_items:
                self.last_item = pygame.time.get_ticks()
                self.items.append(
                    Item(
                        random.randint(100, self.WINDOWS_WIDTH - 100),
                        random.randint(-1000, -100),
                        random.randint(1, 4))
                )

    def handle_keyboard_events(self, keys):
        if keys[pygame.K_UP]:
            print(f">>> Ship.y: {self.ship.y}")
            if self.ship.y >= 0:
                self.ship.y -= self.ship.velocity
        if keys[pygame.K_DOWN]:
            if self.ship.y <= (self.WINDOWS_HEIGHT - self.ship.height):
                self.ship.y += self.ship.velocity
        if keys[pygame.K_LEFT]:
            if self.ship.x >= 0:
                self.ship.x -= self.ship.velocity
        if keys[pygame.K_RIGHT]:
            if self.ship.x <= (self.WINDOWS_WIDTH - self.ship.width):
                self.ship.x += self.ship.velocity
        if keys[pygame.K_SPACE]:
            self.create_bullet()
    
    def remove_enemy(self, enemy):
        try:
            if self.enemies.__contains__(enemy):
                self.enemies.remove(enemy)
                print(f">>> Enemy {enemy} has been removed.")
        except ValueError:
            print(">>> Enemy already removed")

    def create_enemy(self):
        self.enemy_count += 1
        return Enemy(
            self.enemy_count,
            random.randint(0, self.WINDOWS_WIDTH),
            -100,
            random.randint(1,2)
        )

    def play(self):
        print(">>> playing..")
        while self.playing and self.life > 0:
            self.pass_time += self.clock.tick(self.FRAME_PER_SECONDS)
            if self.pass_time > self.time_between_enemies:
                self.enemies.append(self.create_enemy())
                self.pass_time = 0

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.playing = False

            self.create_item()

            pressed_keys = pygame.key.get_pressed()
            self.handle_keyboard_events(pressed_keys)

            self.WINDOW.fill("black")
            self.WINDOW.blit(self.BACKGROUND, (0, 0))
            self.ship.draw(self.WINDOW)

            for enemy in self.enemies:
                enemy.draw(self.WINDOW)
                enemy.move()

                # if Ship crash with the Enemy
                if pygame.Rect.colliderect(self.ship.rect, enemy.rect):
                    self.life -= 1
                    print(f"You have {self.life} life remain.")
                    self.remove_enemy(enemy)

                for bullet in self.bullets:
                    # if the bullet touch the Enemy
                    if pygame.Rect.colliderect(bullet.rect, enemy.rect):
                        enemy.live -= 1
                        self.bullets.remove(bullet)
                        self.score += 1

                if enemy.live <= 0:
                    self.SOUND_DEATH.play()
                    self.remove_enemy(enemy)
                    #print(f"# Enemies {len(self.enemies)} remain.")

                # print(f">>> Enemy.x: {enemy.x}")
                # print(f">>> Enemy.y: {enemy.y}")
                if enemy.y > self.WINDOWS_HEIGHT:
                    self.remove_enemy(enemy)

            for bullet in self.bullets:
                bullet.draw(self.WINDOW)
                bullet.move()

                if bullet.y < 0:
                    #print(f">>> bullet.y: {bullet.y}")
                    self.bullets.remove(bullet)

            for item in self.items:
                item.draw(self.WINDOW)
                item.move()

                # collition detection
                if pygame.Rect.colliderect(item.rect, self.ship.rect):
                    self.items.remove(item)

                    if item.type == 1:
                        self.score += 100
                    elif item.type == 2:
                        self.score += 500
                    elif item.type == 3:
                        self.life += 1
                    else:
                        self.score += 50

                if item.y > self.WINDOWS_HEIGHT:
                    self.items.remove(item)

            text_live = self.FRONT.render(f"Life: {self.life}", True, "white")
            text_points = self.FRONT.render(f"Score: {self.score}", True, "white")

            self.WINDOW.blit(text_live, (20, 20))
            self.WINDOW.blit(text_points, (20, 50))

            pygame.display.update()

        # game over section
        #self.SOUND_DEATH.play()
        self.SOUND_GAME_OVER.play()
        text_game_over = self.FRONT.render(f"Game Over. You score: {self.score}", True, "red")
        self.WINDOW.blit(text_game_over, ( (self.WINDOWS_WIDTH/2 - 250), self.WINDOWS_HEIGHT/3))
        pygame.display.update()
        sleep(10)
        pygame.quit()

        date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        with open('scores.txt', 'a') as _file:
            _file.write(f"{date} - {self.score}\n")
            quit()