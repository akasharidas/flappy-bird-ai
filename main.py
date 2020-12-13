import pygame
import sys
import random


pygame.init()
clock = pygame.time.Clock()
W, H = (int(0.5 * i) for i in (576, 1024))
screen = pygame.display.set_mode((W, H))

# global variables
framerate = 144
g = 0.15
bird_start_x = 50
bird_start_y = H // 2
jump_impulse = 5

if random.randint(0, 1):
    background = pygame.image.load("assets/background-night.png").convert()
else:
    background = pygame.image.load("assets/background-day.png").convert()

floor_surface = pygame.image.load("assets/base.png").convert()
floor_x = 0

bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert()
bird_rect = bird_surface.get_rect(center=(bird_start_x, bird_start_y))
bird_dy = 0


# game loop
while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            bird_dy = -jump_impulse

    # draw background
    screen.blit(background, (0, 0))

    # draw and animate floor
    screen.blit(floor_surface, (floor_x, H - 112))
    screen.blit(floor_surface, (floor_x + W, H - 112))
    floor_x -= 1
    if floor_x <= -W:
        floor_x = 0

    # draw and animate bird
    screen.blit(bird_surface, bird_rect)
    bird_rect.centery += bird_dy
    bird_dy += g

    pygame.display.update()
    clock.tick(framerate)
