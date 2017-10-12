###login window menu

import pygame

pygame.init()
pygame.font.init()

width = 600
height = 800

displayPlane = pygame.display.set_mode((width, height))

pygame.display.set_caption("Login - spoodipy")
clock = pygame.time.Clock()

exitWindow = False

while not exitWindow:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitWindow = True

    displayPlane.
