import pygame
from pygame.locals import *
import random

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                      pygame.image.load('bluebird-midflap.png').convert_alpha(),
                      pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()          # load - Carrega a imagem do pássaro
        self.rect = self.image.get_rect()                                               # convert_alpha() - Identifica que é png (sem fundo)
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2                                                # rect - Tupla com 4 informações (a1, a2, a3, a4)
        self.speed = SPEED
        self.mask = pygame.mask.from_surface(self.image)

                                                                                        # (a1, a2) onde o pássaro está; (a3, a4) o tamanho do pássaro
    def update(self):

        """
        Esse módulo atualiza qual imagem do pássaro aparecerá e onde, na tela, ele estará. A cada volta do while principal
        a imagem a ser exibida é alterada entre uma das três do asset.
        :return:
        """
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]
        self.speed += GRAVITY
        self.mask = pygame.mask.from_surface(self.image)

        """
        Esse rect é o 'retângulo' que define o pássaro. Todos os pixels dele
        """
        self.rect[1] += self.speed
        pass

    def bump(self):
        self.speed = -SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAMESPEED


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAMESPEED


def is_off_screen(sprite):
    return sprite.rect[0] < - sprite.rect[2]


def get_random_pipes(xpos):
    size = random.randint(100, 400)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAMESPEED = 10
GROUND_WIDTH = 2*SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_WIDHT = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
DIST = 1.5

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Define o tamanho(resolução) da tela

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT) )

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH*i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()

i = 0
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH*i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()                                       # Essa classe diminui os fps junto com a clock.tick()

while True:
    clock.tick(30)
    for event in pygame.event.get():                              # Laço principal
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()


    screen.blit(BACKGROUND, (0, 0))                               # A função blit coloca uma imagem em cima de outra

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(2*SCREEN_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * DIST)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    pipe_group.update()
    bird_group.draw(screen)
    pipe_group.draw(screen)

    # if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask):
    #     # Game Over
    #     break

    ground_group.update()
    ground_group.draw(screen)

    pygame.display.update()

    if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask):
        # Game Over
        break
