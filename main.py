import pygame
import sys

pygame.init()
screen = pygame.display.set_mode([int(0.5 * i) for i in (576, 1024)])

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
