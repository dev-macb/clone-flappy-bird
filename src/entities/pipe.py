import random
from src.configuracao import LARGURA_TELA, Y_CHAO, TAMANHO_VAO_TUBO


def obter_par_tubo_aleatorio(gr):
    y_vao = random.randrange(0, int(Y_CHAO * 0.6 - TAMANHO_VAO_TUBO))
    y_vao += int(Y_CHAO * 0.2)
    altura_tubo = gr.imagens['tubo'][0].get_height()
    x_tubo = LARGURA_TELA + 10
    return (
        {'x': x_tubo, 'y': y_vao - altura_tubo},
        {'x': x_tubo, 'y': y_vao + TAMANHO_VAO_TUBO},
    )
