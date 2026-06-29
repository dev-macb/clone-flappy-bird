import pygame
from pygame.locals import KEYDOWN, K_SPACE, K_UP
from src.configuracao import LARGURA_TELA, Y_CHAO
from src.states.state_machine import Estado
from src.systems.score import renderizar_pontuacao


class EstadoFimDeJogo(Estado):
    def entrar(self, **kwargs):
        self.gr = self.jogo.gr
        self.pontuacao = kwargs['pontuacao']
        self.jogador_x = LARGURA_TELA * 0.2
        self.jogador_y = kwargs['y']
        self.jogador_h = self.gr.imagens['jogador'][0].get_height()
        self.jogador_vel_y = kwargs['jogador_vel_y']
        self.jogador_acel_y = 2
        self.jogador_rotacao = kwargs['jogador_rotacao']
        self.jogador_vel_rot = 7
        self.chao_x = kwargs['base_x']
        self.tubos_superiores = kwargs['tubos_superiores']
        self.tubos_inferiores = kwargs['tubos_inferiores']
        self.colisao_chao = kwargs['colisao_chao']
        self.gr.sons['batida'].play()
        if not self.colisao_chao:
            self.gr.sons['morrer'].play()

    def processar_evento(self, evento):
        if evento.type == KEYDOWN and (evento.key == K_SPACE or evento.key == K_UP):
            if self.jogador_y + self.jogador_h >= Y_CHAO - 1:
                from src.states.welcome_state import EstadoBoasVindas
                self.jogo.me.trocar(EstadoBoasVindas(self.jogo))

    def atualizar(self):
        if self.jogador_y + self.jogador_h < Y_CHAO - 1:
            self.jogador_y += min(self.jogador_vel_y, Y_CHAO - self.jogador_y - self.jogador_h)

        if self.jogador_vel_y < 15:
            self.jogador_vel_y += self.jogador_acel_y

        if not self.colisao_chao and self.jogador_rotacao > -90:
            self.jogador_rotacao -= self.jogador_vel_rot

    def renderizar(self, tela):
        tela.blit(self.gr.imagens['fundo'], (0, 0))

        for tSuperior, tInferior in zip(self.tubos_superiores, self.tubos_inferiores):
            tela.blit(self.gr.imagens['tubo'][0], (tSuperior['x'], tSuperior['y']))
            tela.blit(self.gr.imagens['tubo'][1], (tInferior['x'], tInferior['y']))

        tela.blit(self.gr.imagens['chao'], (self.chao_x, Y_CHAO))
        renderizar_pontuacao(tela, self.pontuacao, self.gr)
        superficie_jogador = pygame.transform.rotate(self.gr.imagens['jogador'][1], self.jogador_rotacao)
        tela.blit(superficie_jogador, (self.jogador_x, self.jogador_y))
        tela.blit(self.gr.imagens['fim_de_jogo'], (50, 180))
