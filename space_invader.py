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
        self.x = 400
        self.y = 520
        self.vel_x = 0
        self.vel_y = 0

class Shot(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resources/shot.png")).convert_alpha()

class Player(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("resources/ship.png")).convert_alpha()

print()
print("Press any key to start")

black = (0, 0, 0)

pygame.init()

w, h = 850, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Invader')
screen.fill(black)

background = pygame.image.load(os.path.join("resources/background.png"))
screen.blit(background, (0, 0))

x, y = 400, 500
shot_y = y

fps = pygame.time.Clock()

ship = Player()
w_ship, h_ship = ship.get_size()

all_sprites = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            screen.blit(background, (0, 0))
            x -= 7
        if keys[pygame.K_f]:
            screen.blit(background, (0, 0))
            x += 7
        if keys[pygame.K_SPACE]:
            all_sprites.update()
            screen.blit(background, (0, 0))
            shot = Shot()
            all_sprites.add(shot)
            all_sprites.draw(screen)
        
        screen.blit(ship, (x, y))
    
    fps.tick(60)
    pygame.display.update()

pygame.quit()
sys.exit()
