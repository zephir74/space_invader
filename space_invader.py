#!/usr/bin/env python3

import pygame
import os
import sys
import random

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vel_x, vel_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/ship.png")).convert_alpha(), 400, 520, 0, 0)

class Shot(Sprite):
    def __init__(self, player):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/shot.png")).convert_alpha(), player.rect.midtop[0], player.rect.midtop[1], 0, -10)

class Enemy(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/alien1.png")).convert_alpha(), random.choice(range(10, 850, 10)), 550, 0, 2)

    def laserCollision(self, alien, shot):
        lasercollision = pygame.sprite.collide_rect(alien, shot)
        if lasercollision == True:
            score += 1

    def playerCollision(self, alien, ship):
        playercollision = pygame.sprite.collide_rect(alien, ship)
        if playercollision == True:
            print("Game over...")
            print(f"Your score was : {i}")
            pygame.quit()
            sys.exit()

print()
print("Press any key to start")

black = (0, 0, 0)

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load('resources/space_invader-epic.mp3')
pygame.mixer.music.play(-1)

w, h = 850, 600
screen = pygame.display.set_mode(size=(w, h), vsync=1)
pygame.display.set_caption('Space Invaders')
screen_rect = screen.get_rect()

fps = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

ship = Player()
all_sprites.add(ship)

ship_img = pygame.image.load(os.path.join("resources/ship.png"))
laser = pygame.image.load(os.path.join("resources/shot.png"))

w_ship = ship_img.get_width()
w_shot = laser.get_width()

score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            ship.vel_x = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.vel_x = -7
            if event.key == pygame.K_RIGHT:
                ship.vel_x = 7
            if event.key == pygame.K_SPACE:
                shot = Shot(ship)
                all_sprites.add(shot)
                shot.rect.x, shot.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2), ship.rect.y

                if shot.rect.y < h:
                    shot.kill()
                    print("shot deleted")

    screen.fill(black)
    all_sprites.update()
    all_sprites.draw(screen)

    alien = Enemy()
    all_sprites.add(alien)
    alien.laserCollision(alien, shot)
    alien.playerCollision(alien, ship)

    fps.tick(60)
    pygame.display.update()
    
    for i in score:
        print(f"Your score : {i}")

pygame.quit()
sys.exit()
