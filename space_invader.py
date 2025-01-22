import pygame
import os
import sys

print()
print("Press any key to start")

w, h = 850, 600

pygame.init()

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Space Invader')

screen.fill("black")

fps = pygame.time.Clock()

x, y = 400, 520
velocity = 15

ship = pygame.image.load(os.path.join("resources/ship.png"))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            screen.fill("black")
            x -= 7
        if keys[pygame.K_f]:
            screen.fill("black")
            x += 7
        if keys[pygame.K_SPACE] and y > 0:
            shot = pygame.image.load(os.path.join("resources/shot.png"))
            w_ship, h_ship = ship.get_size()
            w_shot, h_shot = shot.get_size()
            shot_y = y
            screen.blit(shot, (x - int(w_shot / 2) + int(w_ship / 2), shot_y))
            shot_y -= velocity

        screen.blit(ship, (x, y))

    fps.tick(60)
    pygame.display.update()

pygame.quit()
sys.exit()
