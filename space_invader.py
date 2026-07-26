#!/usr/bin/env python3

import pygame
import os
import sys
import random
import time
import threading

score = 980

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

class Player2(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/ship2.png")).convert_alpha(), 400, 520, 0, 0) # class for 2nd ship

    def update(self):
        return super().update()

class Shot(Sprite):
    def __init__(self, player):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/shot.png")).convert_alpha(), player.rect.midtop[0], player.rect.midtop[1], 0, -10)

    def update(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

        return super().update()

class Shot2(Sprite):
    def __init__(self, player):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/shot2.png")).convert_alpha(), player.rect.midtop[0], player.rect.midtop[1], 0, -10)

    def update(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

        return super().update()
    
class Enemy(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/alien1.png")).convert_alpha(), random.choice(range(10, 850, 50)), 50, 0, 1)

    def update(self):
        if not self.rect.colliderect(screen_rect):
            pygame.mixer.stop()
            screen.blit(game_over_bottom, (0, 0))
            show_score = policy.render(f"Your score was : {score}", True, (255, 255, 255))
            screen.blit(show_score, (0, 0))
            pygame.display.update()
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("resources/sounds/player_down.mp3"))
            pygame.mixer.Channel(3).set_volume(1.0)
            time.sleep(3)
            exit()

        return super().update()

class Enemy2(Sprite):
    def __init__(self):
        Sprite.__init__(self, pygame.image.load(os.path.join("resources/alien2.png")).convert_alpha(), random.choice(range(10, 850, 50)), 50, random.choice([-1, 1]), 0)
        
    last_y_pos = int()
    executed = False

    def update(self):
        if self.rect.x >= 800:            
            if not self.executed:
                self.executed = True
                self.last_y_pos = self.rect.y
                self.vel_x = 0
                self.vel_y = 1

            if self.rect.y - self.last_y_pos >= 100:
                self.executed = False
                self.vel_y = 0
                self.vel_x = -1

        if self.rect.x <= 50:
            if not self.executed:
                self.executed = True
                self.last_y_pos = self.rect.y
                self.vel_x = 0
                self.vel_y = 1

            if self.rect.y - self.last_y_pos >= 100:
                self.executed = False
                self.vel_y = 0
                self.vel_x = 1

        if not self.rect.colliderect(screen_rect):
            pygame.mixer.stop()
            screen.blit(game_over_bottom, (0, 0))
            show_score = policy.render(f"Your score was : {score}", True, (255, 255, 255))
            screen.blit(show_score, (0, 0))
            pygame.display.update()
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("resources/sounds/player_down.mp3"))
            pygame.mixer.Channel(3).set_volume(1.0)
            time.sleep(3)
            exit()

        return super().update()
    
black = (0, 0, 0)

pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.Channel(0).play(pygame.mixer.Sound("resources/sounds/space_invader-epic.mp3"))

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
pygame.time.set_timer(enemy_event, 900)

enemy2_event = pygame.event.custom_type() 
pygame.time.set_timer(enemy2_event, 1500)

policy = pygame.font.SysFont('Comic Sans MS', 32)
game_over_bottom = pygame.image.load(os.path.join("resources/game_over_bottom.jpg"))
game_over_touched = pygame.image.load(os.path.join("resources/game_over_touched.jpg"))

running = True
new_ship = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP:
            ship.vel_x = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ship.vel_x = -8
            if event.key == pygame.K_RIGHT:
                ship.vel_x = 8
            if event.key == pygame.K_SPACE:
                if score < 1000:
                    shot = Shot(ship)
                    shot.rect.x, shot.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2), ship.rect.y
                    shots_group.add(shot)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/shoot.mp3"))
                    pygame.mixer.Channel(1).set_volume(1.0)
                else:
                    shot_left = Shot2(ship)
                    shot_middle = Shot2(ship)
                    shot_right = Shot2(ship)
                    
                    shot_left.rect.x, shot_left.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2) - 40, ship.rect.y
                    shot_middle.rect.x, shot_middle.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2), ship.rect.y
                    shot_right.rect.x, shot_right.rect.y = ship.rect.x - int(w_shot / 2) + int(w_ship / 2) + 40, ship.rect.y
                    
                    shots_group.add(shot_left)
                    shots_group.add(shot_middle)
                    shots_group.add(shot_right)
                    
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("resources/sounds/shoot.mp3"))
                    pygame.mixer.Channel(1).set_volume(1.0)
                
        if event.type == enemy_event:
            alien = Enemy()
            enemy_group.add(alien)

        if score >= 500 and event.type == enemy2_event:
            alien2 = Enemy2()
            enemy_group.add(alien2)

        if score == 1000 and new_ship != True: # upgrade ship
            new_ship = True
            player_group.remove(ship)
            ship = Player2()
            player_group.add(ship)
        
    screen.fill(black)

    player_group.update()
    shots_group.update(screen_rect)

    if pygame.sprite.groupcollide(shots_group, enemy_group, True, True, collided=None):
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("resources/sounds/alien_down.wav"))
        pygame.mixer.Channel(2).set_volume(0.3)
        score += 10

    if pygame.sprite.groupcollide(player_group, enemy_group, True, True, collided=None):
        pygame.mixer.stop()
        screen.blit(game_over_bottom, (0, 0))
        show_score = policy.render(f"Your score was : {score}", True, (255, 255, 255))
        screen.blit(show_score, (0, 0))
        pygame.display.update()
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("resources/sounds/player_down.mp3"))
        pygame.mixer.Channel(3).set_volume(1.0)
        time.sleep(3)
        break

    player_group.draw(screen)
    shots_group.draw(screen)

    enemy_group.update()
    enemy_group.draw(screen)

    show_score = policy.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(show_score, (0, 0))

    fps.tick(60)
    pygame.display.update()

pygame.quit()
sys.exit()
