from itertools import cycle
from pygame.locals import KEYDOWN, K_SPACE, K_UP
from src.configuracao import LARGURA_TELA, ALTURA_TELA
from src.entities.base import Chao
from src.states.state_machine import Estado


class EstadoBoasVindas(Estado):
    def entrar(self, **kwargs):
        self.gr = self.jogo.gr
        self.gr.aleatorizar()
        self.indice_jogador = 0
        self.gerador_indice_jogador = cycle([0, 1, 2, 1])
        self.iter_loop = 0
        self.jogador_x = int(LARGURA_TELA * 0.2)
        self.jogador_y = int((ALTURA_TELA - self.gr.imagens['jogador'][0].get_height()) / 2)
        self.mensagem_x = int((LARGURA_TELA - self.gr.imagens['mensagem'].get_width()) / 2)
        self.mensagem_y = int(ALTURA_TELA * 0.12)
        self.chao = Chao(self.gr)
        self.chao.reiniciar()
        self.valor_osc = 0
        self.dir_osc = 1


    def processar_evento(self, evento):
        if evento.type == KEYDOWN and (evento.key == K_SPACE or evento.key == K_UP):
            self.gr.sons['asa'].play()
            from src.states.play_state import EstadoJogo
            self.jogo.me.trocar(
                EstadoJogo(self.jogo),
                jogador_y=self.jogador_y + self.valor_osc,
                base_x=self.chao.x,
                gerador_indice_jogador=self.gerador_indice_jogador,)


    def atualizar(self):
        if (self.iter_loop + 1) % 5 == 0:
            self.indice_jogador = next(self.gerador_indice_jogador)

        self.iter_loop = (self.iter_loop + 1) % 30
        self.chao.atualizar()

        if abs(self.valor_osc) == 8:
            self.dir_osc *= -1

        self.valor_osc += self.dir_osc

    def renderizar(self, tela):
        tela.blit(self.gr.imagens['fundo'], (0, 0))
        tela.blit(self.gr.imagens['jogador'][self.indice_jogador], (self.jogador_x, self.jogador_y + self.valor_osc))
        tela.blit(self.gr.imagens['mensagem'], (self.mensagem_x, self.mensagem_y))
        self.chao.desenhar(tela)
