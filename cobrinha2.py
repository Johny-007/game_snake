from sys import exit
from random import randint
import pygame
from pygame.locals import *
from pygame.surface import Surface, SurfaceType

pygame.init() #execuçao

# VARIAVEIS

x_tela = 640
y_tela = 480

corBranco = (255, 255, 255)
corPreto = (0, 0, 0)
corCobra = (0, 157, 5)

tela: Surface | SurfaceType = pygame.display.set_mode((x_tela, y_tela))
pygame.display.set_caption('JOGO DA COBRINHA')     #execuçao

cobra_x = x_tela / 2
cobra_y = y_tela / 2

imagem_inicio = pygame.image.load('cobrinha01.png').convert()
imagem_inicio = pygame.transform.scale(imagem_inicio, (200, 60))
tela_inicio = pygame.image.load('tela_inicio.png').convert()
tela_inicio = pygame.transform.scale((tela_inicio), (260, 220))

x_maca = randint(40, 600)
y_maca = randint(40, 420)

pontos = 0
fonte1 = pygame.font.SysFont('arial', 25, True, True)
fonte2 = pygame.font.SysFont('arial', 15, True, True)
fonte3 = pygame.font.SysFont('gadugi', 23, True, True)

pygame.mixer.music.set_volume(0.07)      #exe
musica = pygame.mixer.music.load("X2Download.com - Música Celta (A Música dos deuses) (128 kbps).mp3")
pygame.mixer.music.play(-1)              #exe
colisao01 = pygame.mixer.Sound('beep-03.wav')

clock = pygame.time.Clock()

lista_cobra = []
cobra_cauda = 3

vel = 9
x_controle = vel
y_controle = 0

morreu = False


# DEF'S
def mensagem_tela(mensagem, fonte, cor, eixo_X, eixo_Y):
    texto_atu = fonte.render(mensagem, True, cor)
    tela.blit(texto_atu, (eixo_X, eixo_Y))


def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 157, 5), (XeY[0], XeY[1], 25, 25))

def reiniciar():
    global pontos, cobra_y, cobra_x, cobra_cauda, lista_cobra, lista_cabeca, x_maca, y_maca, morreu
    pontos = 0
    cobra_x = x_tela / 2
    cobra_y = y_tela / 2
    cobra_cauda = 3
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(40, 420)
    morreu = False


# LOOPING INICIAL
iniciar = True
while iniciar:
    tela.fill((0, 0, 0))
    tela.blit(imagem_inicio, (220, 20))
    tela.blit(tela_inicio, (190, 145))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_f:
                iniciar = False
    pygame.display.flip()

musica = pygame.mixer.music.load('trilhasonora.mp3.mp3')
pygame.mixer.music.play(-1)
# LOOPING PRINCIPAL
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == vel:
                    pass
                else:
                    x_controle = -vel
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -vel:
                    pass
                else:
                    x_controle = vel
                    y_controle = 0
            if event.key == K_w:
                if y_controle == vel:
                    pass
                else:
                    y_controle = -vel
                    x_controle = 0
            if event.key == K_s:
                if y_controle == vel:
                    pass
                else:
                    y_controle = vel
                    x_controle = 0
    cobra_x = cobra_x + x_controle
    cobra_y = cobra_y + y_controle

    tela.fill((0, 230, 0))
    pygame.draw.rect(tela, (0, 0, 0), (0, 0, x_tela, 40))
    aumenta_cobra(lista_cobra)
    mensagem_tela(f"Pontos: {pontos}", fonte1, corBranco, 22, 5)

    # DESENHO
    cobra = pygame.draw.rect(tela, corCobra, (cobra_x, cobra_y, 25, 25))
    maca = pygame.draw.rect(tela, (200, 5, 5), (x_maca, y_maca, 25, 25))
    pygame.display.update()

    # COLISAO
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(40, 420)
        pontos = pontos + 1
        colisao01.play()
        cobra_cauda = cobra_cauda + 1

    # COBRA
    lista_cabeca = []
    lista_cabeca.append(cobra_x)
    lista_cabeca.append(cobra_y)
    lista_cobra.append(lista_cabeca)

    if len(lista_cobra) > cobra_cauda:
        del lista_cobra[0]

    if cobra_x >= x_tela + 2:
        cobra_x = 0
    if cobra_x <= -2:
        cobra_x = x_tela
    if cobra_y >= y_tela + 2:
        cobra_y = 42
    if cobra_y <= 40:
        cobra_y = y_tela




    #GAME OVER
    if lista_cobra.count(lista_cabeca) > 1:
        morreu = True
        while morreu:
            tela.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar()
            mensagem_tela(f' Voce capturou {pontos} pontos!! mas infelizmente perdeu. Pressione R para voltar', fonte2, corPreto, 45, 240)
            pygame.display.update()


    # FUNCAO
    clock.tick(30)
