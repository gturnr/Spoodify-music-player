import pygame

pygame.init()
pygame.font.init()


font = pygame.font.SysFont('Arial', 30)
boldfont = pygame.font.SysFont('Arial', 50)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)

display_width = 576
display_height = 1024

Display = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Login')
clock = pygame.time.Clock()


def login()


Exit = False

while not Exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Exit = True

pygame.quit()
exit()