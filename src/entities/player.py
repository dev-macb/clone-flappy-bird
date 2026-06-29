import pygame
from itertools import cycle
from src.configuracao import JOGADOR_X, JOGADOR_ACEL_BATIDA, JOGADOR_VEL_Y_MAXIMO, JOGADOR_ACEL_Y, Y_CHAO


class Jogador:
    def __init__(self, gr, y=0):
        self.gr = gr
        self.x = JOGADOR_X
        self.y = y
        self.vel_y = -9
        self.rotacao = 45
        self.indice = 0
        self.gerador_indice = cycle([0, 1, 2, 1])
        self.iter_loop = 0
        self.bateu = False


    def bater(self):
        if self.y > -2 * self.gr.imagens['jogador'][0].get_height():
            self.vel_y = JOGADOR_ACEL_BATIDA
            self.bateu = True


    def atualizar(self):
        if (self.iter_loop + 1) % 3 == 0:
            self.indice = next(self.gerador_indice)
        self.iter_loop = (self.iter_loop + 1) % 30
        if self.rotacao > -90:
            self.rotacao -= 3
        if self.vel_y < JOGADOR_VEL_Y_MAXIMO and not self.bateu:
            self.vel_y += JOGADOR_ACEL_Y
        if self.bateu:
            self.bateu = False
            self.rotacao = 45
        altura_jogador = self.gr.imagens['jogador'][self.indice].get_height()
        self.y += min(self.vel_y, Y_CHAO - self.y - altura_jogador)


    def obter_rot_visivel(self):
        return min(self.rotacao, 20)


    def desenhar(self, tela):
        rot_visivel = self.obter_rot_visivel()
        superficie = pygame.transform.rotate(self.gr.imagens['jogador'][self.indice], rot_visivel)
        tela.blit(superficie, (self.x, self.y))
