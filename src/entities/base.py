from src.configuracao import Y_CHAO


class Chao:
    def __init__(self, gr):
        self.gr = gr
        self.x = 0
        self._deslocamento = gr.imagens['chao'].get_width() - gr.imagens['fundo'].get_width()

    def reiniciar(self):
        self.x = 0

    def atualizar(self, velocidade=100):
        self.x = -((-self.x + velocidade) % self._deslocamento)

    def desenhar(self, tela):
        tela.blit(self.gr.imagens['chao'], (self.x, Y_CHAO))
