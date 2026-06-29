import pygame
from itertools import cycle
from pygame.locals import KEYDOWN, K_SPACE, K_UP
from src.configuracao import LARGURA_TELA, Y_CHAO
from src.entities.base import Chao
from src.entities.pipe import obter_par_tubo_aleatorio
from src.states.state_machine import Estado
from src.systems.collision import verificarColisao
from src.systems.score import renderizar_pontuacao


class EstadoJogo(Estado):
    def entrar(self, **kwargs):
        self.gr = self.jogo.gr
        self.pontuacao = 0
        self.indice_jogador = 0
        self.iter_loop = 0
        self.gerador_indice_jogador = kwargs.get('gerador_indice_jogador', cycle([0, 1, 2, 1]))
        self.jogador_x = int(LARGURA_TELA * 0.2)
        self.jogador_y = kwargs['jogador_y']
        self.chao = Chao(self.gr)
        self.chao.x = kwargs['base_x']
        superior1, inferior1 = obter_par_tubo_aleatorio(self.gr)
        superior2, inferior2 = obter_par_tubo_aleatorio(self.gr)
        self.tubos_superiores = [
            {'x': LARGURA_TELA + 200, 'y': superior1['y']},
            {'x': LARGURA_TELA + 200 + LARGURA_TELA / 2, 'y': superior2['y']},
        ]
        self.tubos_inferiores = [
            {'x': LARGURA_TELA + 200, 'y': inferior1['y']},
            {'x': LARGURA_TELA + 200 + LARGURA_TELA / 2, 'y': inferior2['y']},
        ]
        self.jogador_vel_y = -9
        self.jogador_vel_y_maximo = 10
        self.jogador_acel_y = 1
        self.jogador_rotacao = 45
        self.jogador_vel_rot = 3
        self.jogador_limiar_rot = 20
        self.jogador_acel_batida = -9
        self.jogador_bateu = False


    def processar_evento(self, evento):
        if evento.type == KEYDOWN and (evento.key == K_SPACE or evento.key == K_UP):
            if self.jogador_y > -2 * self.gr.imagens['jogador'][0].get_height():
                self.jogador_vel_y = self.jogador_acel_batida
                self.jogador_bateu = True
                self.gr.sons['asa'].play()


    def atualizar(self):
        colisao = verificarColisao(self.jogador_x,                     
            self.jogador_y, 
            self.indice_jogador, 
            self.tubos_superiores, 
            self.tubos_inferiores, 
            self.gr)
        
        if colisao[0]:
            from src.states.gameover_state import EstadoFimDeJogo
            self.jogo.me.trocar(
                EstadoFimDeJogo(self.jogo),
                y=self.jogador_y, colisao_chao=colisao[1],
                base_x=self.chao.x, tubos_superiores=self.tubos_superiores,
                tubos_inferiores=self.tubos_inferiores, pontuacao=self.pontuacao,
                jogador_vel_y=self.jogador_vel_y, jogador_rotacao=self.jogador_rotacao,)
            return
        
        meio_jogador = self.jogador_x + self.gr.imagens['jogador'][0].get_width() / 2

        for tubo in self.tubos_superiores:
            meio_tubo = tubo['x'] + self.gr.imagens['tubo'][0].get_width() / 2
            if meio_tubo <= meio_jogador < meio_tubo + 4:
                self.pontuacao += 1
                self.gr.sons['ponto'].play()

        if (self.iter_loop + 1) % 3 == 0:
            self.indice_jogador = next(self.gerador_indice_jogador)

        self.iter_loop = (self.iter_loop + 1) % 30
        self.chao.atualizar()

        if self.jogador_rotacao > -90:
            self.jogador_rotacao -= self.jogador_vel_rot

        if self.jogador_vel_y < self.jogador_vel_y_maximo and not self.jogador_bateu:
            self.jogador_vel_y += self.jogador_acel_y

        if self.jogador_bateu:
            self.jogador_bateu = False
            self.jogador_rotacao = 45

        altura_jogador = self.gr.imagens['jogador'][self.indice_jogador].get_height()
        self.jogador_y += min(self.jogador_vel_y, Y_CHAO - self.jogador_y - altura_jogador)

        for tSuperior, tInferior in zip(self.tubos_superiores, self.tubos_inferiores):
            tSuperior['x'] -= 4
            tInferior['x'] -= 4

        if len(self.tubos_superiores) > 0 and 0 < self.tubos_superiores[0]['x'] < 5:
            superior, inferior = obter_par_tubo_aleatorio(self.gr)
            self.tubos_superiores.append(superior)
            self.tubos_inferiores.append(inferior)

        largura_tubo = self.gr.imagens['tubo'][0].get_width()
        if len(self.tubos_superiores) > 0 and self.tubos_superiores[0]['x'] < -largura_tubo:
            self.tubos_superiores.pop(0)
            self.tubos_inferiores.pop(0)


    def renderizar(self, tela):
        tela.blit(self.gr.imagens['fundo'], (0, 0))
        for tSuperior, tInferior in zip(self.tubos_superiores, self.tubos_inferiores):
            tela.blit(self.gr.imagens['tubo'][0], (tSuperior['x'], tSuperior['y']))
            tela.blit(self.gr.imagens['tubo'][1], (tInferior['x'], tInferior['y']))

        self.chao.desenhar(tela)
        renderizar_pontuacao(tela, self.pontuacao, self.gr)
        rot_visivel = self.jogador_limiar_rot

        if self.jogador_rotacao <= self.jogador_limiar_rot:
            rot_visivel = self.jogador_rotacao

        superficie_jogador = pygame.transform.rotate(self.gr.imagens['jogador'][self.indice_jogador], rot_visivel)
        tela.blit(superficie_jogador, (self.jogador_x, self.jogador_y))
