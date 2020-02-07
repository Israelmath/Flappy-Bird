import pygame
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Define o tamanho(resolução) da tela

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT) )

while True:

    for event in pygame.event.get():                              # Laço principal
        if event.type == QUIT:
            pygame.quit()
    pygame.display.update()

    screen.blit(BACKGROUND, (0, 0))                               # A função blit coloca uma imagem em cima de outra
    