import pygame
from src.configuracao import Y_CHAO


def obterMascara(imagem):
    mascara = []
    
    for x in range(imagem.get_width()):
        mascara.append([])
        for y in range(imagem.get_height()):
            mascara[x].append(bool(imagem.get_at((x, y))[3]))

    return mascara


def colisao_pixel(rect1, rect2, mascara1, mascara2):
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if mascara1[x1 + x][y1 + y] and mascara2[x2 + x][y2 + y]:
                return True

    return False


def verificarColisao(px, py, indice_jogador, tubos_superiores, tubos_inferiores, gr):
    altura_jogador = gr.imagens['jogador'][0].get_height()
    largura_jogador = gr.imagens['jogador'][0].get_width()

    if py + altura_jogador >= Y_CHAO - 1:
        return (True, True)

    rect_jogador = pygame.Rect(px, py, largura_jogador, altura_jogador)
    largura_tubo = gr.imagens['tubo'][0].get_width()
    altura_tubo = gr.imagens['tubo'][0].get_height()

    for tSuperior, tInferior in zip(tubos_superiores, tubos_inferiores):
        rect_superior = pygame.Rect(tSuperior['x'], tSuperior['y'], largura_tubo, altura_tubo)
        rect_inferior = pygame.Rect(tInferior['x'], tInferior['y'], largura_tubo, altura_tubo)
        col_superior = colisao_pixel(rect_jogador, rect_superior, gr.mascaras['jogador'][indice_jogador], gr.mascaras['tubo'][0])
        col_inferior = colisao_pixel(rect_jogador, rect_inferior, gr.mascaras['jogador'][indice_jogador], gr.mascaras['tubo'][1])

        if col_superior or col_inferior:
            return (True, False)

    return (False, False)
