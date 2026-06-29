from src.configuracao import LARGURA_TELA, ALTURA_TELA


def renderizar_pontuacao(tela, pontuacao, gr):
    digitos = [int(x) for x in str(pontuacao)]
    largura_total = sum(gr.imagens['numeros'][d].get_width() for d in digitos)
    x = (LARGURA_TELA - largura_total) / 2

    for d in digitos:
        tela.blit(gr.imagens['numeros'][d], (x, ALTURA_TELA * 0.1))
        x += gr.imagens['numeros'][d].get_width()
