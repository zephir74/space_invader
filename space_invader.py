#!/usr/bin/env python3

import pygame
import os
import sys
import random

score = 490

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

    def update(self):
        return super().update()

class Shot(Sprite):
    def __init__(self, player):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/shot.png")).convert_alpha(), player.rect.midtop[0], player.rect.midtop[1], 0, -10)

    def update(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

        return super().update()

class Enemy(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/alien1.png")).convert_alpha(), random.choice(range(10, 850, 50)), 50, 0, 1)

    def update(self):
        if not self.rect.colliderect(screen_rect):
            print("\nGame over, an alien reached the bottom of the window !\n")
            print(f"Your score was : {score}")
            exit()

        return super().update()

class Enemy2(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/alien2.png")).convert_alpha(), random.choice(range(10, 850, 50)), 50, 0, 0)
        
    last_y_pos = int()
    executed = False

    def update(self, executed=executed):
        self.vel_x = 1 

        if self.rect.x >= 800:
            print(f"right test {executed}")
            
            if not executed:
                last_y_pos = self.rect.y
                executed = True
                print(f"last y pos: {last_y_pos}")
                self.vel_x = 0
                self.vel_y = 1

            if self.rect.y - last_y_pos >= 100:
                self.vel_y = 0
                self.vel_x = -1
                    
        if self.rect.x <= 50:
            print(f"left test {executed}")
            
            if not executed:
                executed = True
                last_y_pos = self.rect.y
                self.vel_x = 0
                self.vel_y = 1

            if self.rect.y - last_y_pos >= 100:
                self.vel_y = 0
                self.vel_x = 1

        if not self.rect.colliderect(screen_rect):
            print("\nGame over, an alien reached the bottom of the window !\n")
            print(f"Your score was : {score}")
            exit()

        return super().update()

print("\nPress any key to start")

black = (0, 0, 0)

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("resources/sounds/space_invader-epic.mp3")
pygame.mixer.music.play(-1)

w, h = 850, 600
screen = pygame.display.set_mode(size=(w, h), vsync=1)
pygame.display.set_caption("Space Invaders")
screen_rect = screen.get_rect()

fps = pygame.time.Clock()

player_group = pygame.sprite.Group()
shots_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

ship = Player()
player_group.add(ship)

ship_img = pygame.image.load(os.path.join("resources/ship.png"))
laser = pygame.image.load(os.path.join("resources/shot.png"))

w_ship = ship_img.get_width()
w_shot = laser.get_width()

enemy_event = pygame.event.custom_type()
pygame.time.set_timer(enemy_event, 2000)

#enemy2_event = pygame.event.custom_type() 
#pygame.time.set_timer(enemy2_event, 1200)

alien2 = Enemy2()
enemy_group.add(alien2)

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
                shot.rect.x, shot.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2), ship.rect.y
                shots_group.add(shot)

        if event.type == enemy_event:
            alien = Enemy()
            enemy_group.add(alien)

        #if score >= 500 and event.type == enemy2_event:
        #    alien2 = Enemy2()
        #    enemy_group.add(alien2)

    screen.fill(black)

    player_group.update()
    shots_group.update(screen_rect)

    if pygame.sprite.groupcollide(shots_group, enemy_group, True, True, collided=None):
        score += 10

    if pygame.sprite.groupcollide(player_group, enemy_group, True, True, collided=None):
        print("\nGame over, you got touched by an alien !\n")
        break

    player_group.draw(screen)
    shots_group.draw(screen)

    enemy_group.update()
    enemy_group.draw(screen)

    fps.tick(60)
    pygame.display.update()

print(f"Your score was : {score}")

pygame.quit()
sys.exit()
