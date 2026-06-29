class Estado:
    def __init__(self, jogo):
        self.jogo = jogo

    def entrar(self, **kwargs):
        pass

    def sair(self):
        pass

    def processar_evento(self, evento):
        pass

    def atualizar(self):
        pass

    def renderizar(self, tela):
        pass


class MaquinaEstado:
    def __init__(self):
        self._estados = []


    @property
    def atual(self):
        return self._estados[-1] if self._estados else None


    def trocar(self, estado_cls, **kwargs):
        if self._estados:
            self._estados[-1].sair()
        self._estados = [estado_cls]
        self._estados[-1].entrar(**kwargs)


    def processar_evento(self, evento):
        if self.atual:
            self.atual.processar_evento(evento)


    def atualizar(self):
        if self.atual:
            self.atual.atualizar()


    def renderizar(self, tela):
        if self.atual:
            self.atual.renderizar(tela)
