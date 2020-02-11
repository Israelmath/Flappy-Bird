import pygame
from pygame.locals import *
import random


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]
        # print('Passou por aqui')

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        # load - Carrega a imagem do pássaro
        self.rect = self.image.get_rect()  # convert_alpha() - Identifica que é png (sem fundo)
        self.rect[0] = (SCREEN_WIDTH - 200) / 2
        self.rect[1] = SCREEN_HEIGHT / 2  # rect - Tupla com 4 informações (a1, a2, a3, a4)
        self.speed = SPEED
        self.mask = pygame.mask.from_surface(self.image)
        self.rotate = ROTATE

        # (a1, a2) onde o pássaro está; (a3, a4) o tamanho do pássaro

    def update(self):
        """
        Esse módulo atualiza qual imagem do pássaro aparecerá e onde, na tela, ele estará. A cada volta do while principal
        a imagem a ser exibida é alterada entre uma das três do asset.
        :return:
        """

        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, self.rotate)
        self.rotate += ROTATE

        """
        Esse rect é o 'retângulo' que define o pássaro. Todos os pixels dele
        """
        self.rect[1] += self.speed
        pass

    def bump(self):
        SOUNDS['bump'].play()
        self.speed = -SPEED
        self.rotate = -(ROTATE*12)


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


class Placar(pygame.sprite.Sprite):

    def __init__(self, number, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('0.png').convert_alpha(),
                       pygame.image.load('1.png').convert_alpha(),
                       pygame.image.load('2.png').convert_alpha(),
                       pygame.image.load('3.png').convert_alpha(),
                       pygame.image.load('4.png').convert_alpha(),
                       pygame.image.load('5.png').convert_alpha(),
                       pygame.image.load('6.png').convert_alpha(),
                       pygame.image.load('7.png').convert_alpha(),
                       pygame.image.load('8.png').convert_alpha(),
                       pygame.image.load('9.png').convert_alpha()]

        self.image = self.images[number]
        self.rect = self.image.get_rect()
        # print(self.images.get_rect())
        self.rect[0] = xpos
        self.rect[1] = 10

    def update(self, score, placar):
        score = str(score)

        if len(score) == 1:
            placar.sprites()[0].image = self.images[int(score[0])]
        elif len(score) == 2:
            placar.sprites()[0].image = self.images[int(score[1])]
            placar.sprites()[1].image = self.images[int(score[0])]
        else:
            placar.sprites()[0].image = self.images[int(score[2])]
            placar.sprites()[1].image = self.images[int(score[1])]
            placar.sprites()[2].image = self.images[int(score[0])]

            # self.image = self.images[score_count(score)]


def is_off_screen(sprite):
    """
    Função que calcula se um sprite saiu da tela

    :param sprite: Parâmetro que pode ser um cano ou um 'chão'.
    :return: True ou False se o sprite saiu ou não da tela.
    """
    return sprite.rect[0] < - sprite.rect[2]


def get_random_pipes(xpos):
    """
    Função que retorna um par de canos em uma altura aleatória, contando com o espaço entre eles para o
    pássaro passar
    :param xpos: Posição, em x, do cano a ser gerado
    :return: Tupla com um par de canos. Um virado para cima e o outro invertido
    """
    size = random.randint(100, 400)
    # size = 200
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


SOUNDS = {}

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1  
GAMESPEED = 10
GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_WIDHT = 80
PIPE_HEIGHT = 500
PIPE_GAP = 200
DIST = 1.9
PLACAR_WIDTH = 24
PLACAR_HEIGHT = 36
ROTATE = -(GRAVITY * 1.5)


# SOUNDS['die'] = pygame.mixer.Sound('die.ogg')SOUNDS['bump'] = pygame.mixer.Sound('wing.ogg')


def main():

    count = 0
    pygame.mixer.pre_init(22100, -16, 2, 64)
    # pygame.mixer.init(22100, -16, 2, 64)
    pygame.init()

    SOUNDS['die'] = pygame.mixer.Sound('die.ogg')
    SOUNDS['bump'] = pygame.mixer.Sound('wing.ogg')
    SOUNDS['point'] = pygame.mixer.Sound('ponto.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('hit.ogg')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Define o tamanho(resolução) da tela

    BACKGROUND = pygame.image.load('background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

    """
    Abaixo temos as linhas que criam, um grupo dos pássaros, criação
    e atribuição de um pássaro e adição desse pássaro ao grupo dos pássaros
    """
    bird_group = pygame.sprite.Group()
    bird = Bird()
    bird_group.add(bird)

    """
    Abaixo temos as linhas que criam, um grupo dos 'chãos', criação e atribuição de um
     'chão' já com a sua posição. Dentro do 'for' é criado mais um chão e adicionado ao
     grupo porque depois excluiremos um deles e adicionaremos outro a uma fila infinita depois de 
     checar se um deles saiu da tela.
    """
    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    """
    Abaixo temos as linhas que criam, um grupo dos canos, uma função, dentro do 'for' para criar
    dois pares de canos em alturas aleatórias pelo mesmo motivo dos chãos. 
    """
    pipe_group = pygame.sprite.Group()
    i = 0
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    """
    Abaixo temos a linha que cria o placar
    """
    score_group = pygame.sprite.Group()
    score = []
    for i in range(3):
        placar = Placar(0, SCREEN_WIDTH - PLACAR_WIDTH * (i + 1) - 10)
        score.append(placar)
    score_group.add(score[0])
    score_group.add(score[1])
    score_group.add(score[2])

    clock = pygame.time.Clock()  # Essa classe diminui os fps junto com a clock.tick()

    pontos = 0

    while True:
        count += 1
        clock.tick(30)
        for event in pygame.event.get():  # Laço principal
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    bird.bump()

        screen.blit(BACKGROUND, (0, 0))  # A função blit coloca uma imagem em cima de outra

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(2 * SCREEN_WIDTH - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(SCREEN_WIDTH * DIST)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        if pipe_group.sprites()[0].rect[0] == SCREEN_WIDTH / 2:
            SOUNDS['point'].play()
            # print(pontos)
            pontos += 1

        bird_group.update()
        pipe_group.update()
        ground_group.update()

        score_group.update(pontos, score_group)
        score_group.draw(screen)
        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        # if pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask):
        #     # Game Over
        #     break

        if pygame.sprite.groupcollide(bird_group, ground_group, False, False,
                                      pygame.sprite.collide_mask) or pygame.sprite.groupcollide(bird_group, pipe_group,
                                                                                                False, False,
                                                                                                pygame.sprite.collide_mask):
            SOUNDS['die'].play()

            # Game Over
            break

    print(count)
main()