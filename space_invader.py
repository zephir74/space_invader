#!/usr/bin/env python3

import pygame
import os
import sys

laser = pygame.image.load(os.path.join("resources/shot.png"))
w_shot, h_shot = laser.get_size()

velocity = 0

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vel_x, vel_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y

class Shot(Sprite):
    def __init__(self, player):
        rect = player.image.get_rect()
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/shot.png")).convert_alpha(), rect.midtop.x, rect.midtop.y, 0, 0)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/ship.png")).convert_alpha(), 400, 520, 0, 0)

print()
print("Press any key to start")

black = (0, 0, 0)

pygame.init()

w, h = 850, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Invader')

fps = pygame.time.Clock()

ship = Player()

all_sprites = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            ship.vel_x -= 7
        if keys[pygame.K_f]:
            ship.vel_x += 7
        if keys[pygame.K_SPACE]:
            shot = Shot(ship)
            all_sprites.add(shot)
    
    fps.tick(60)
    pygame.display.update()

pygame.quit()
sys.exit()
