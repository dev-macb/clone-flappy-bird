import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from src.configuracao import LARGURA_TELA, ALTURA_TELA, FPS, ICONE
from src.engine.gerenciador_de_recursos import GerenciadorRecursos
from src.states.state_machine import MaquinaEstado
from src.states.welcome_state import EstadoBoasVindas


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption('Flappy Bird')
        icone = pygame.image.load(str(ICONE))
        pygame.display.set_icon(icone)
        self.relogio = pygame.time.Clock()
        self.gr = GerenciadorRecursos()
        self.gr.carregar()
        self.me = MaquinaEstado()


    def executar(self):
        self.me.trocar(EstadoBoasVindas(self))
        while True:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    self._sair()

                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    self._sair()

                self.me.processar_evento(evento)

            self.me.atualizar()
            self.me.renderizar(self.tela)
            pygame.display.flip()
            self.relogio.tick(FPS)


    def _sair(self):
        pygame.quit()
        sys.exit()
