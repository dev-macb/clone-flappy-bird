import sys
import random
import pygame
from src.configuracao import (
    SPRITES, AUDIO, FUNDOS, SPRITES_JOGADOR,
    TUBOS, NUMEROS, SPRITE_FIM_DE_JOGO, SPRITE_MENSAGEM, SPRITE_CHAO,
)
from src.systems.collision import obterMascara


class GerenciadorRecursos:
    def __init__(self):
        self.imagens = {}
        self.sons = {}
        self.mascaras = {}
        self._carregado = False


    def carregar(self):
        if self._carregado:
            return
        
        self._carregado = True
        self._carregar_numeros()
        self._carregar_estaticos()
        self._carregar_sons()


    def _carregar_numeros(self):
        self.imagens['numeros'] = tuple(
            pygame.image.load(str(SPRITES / nome)).convert_alpha()
            for nome in NUMEROS
        )


    def _carregar_estaticos(self):
        self.imagens['fim_de_jogo'] = pygame.image.load(str(SPRITES / SPRITE_FIM_DE_JOGO)).convert_alpha()
        self.imagens['mensagem'] = pygame.image.load(str(SPRITES / SPRITE_MENSAGEM)).convert_alpha()
        self.imagens['chao'] = pygame.image.load(str(SPRITES / SPRITE_CHAO)).convert_alpha()


    def _carregar_sons(self):
        ext = '.wav' if 'win' in sys.platform else '.ogg'
        arquivos = ('morrer', 'batida', 'ponto', 'swoosh', 'asa')
        nomes_arquivo = ('die', 'hit', 'point', 'swoosh', 'wing')
        for chave, nome_arquivo in zip(arquivos, nomes_arquivo):
            self.sons[chave] = pygame.mixer.Sound(str(AUDIO / f'{nome_arquivo}{ext}'))


    def selecionar_fundo(self):
        nome = random.choice(FUNDOS)
        self.imagens['fundo'] = pygame.image.load(str(SPRITES / nome)).convert()


    def selecionar_sprites_jogador(self):
        sprites = random.choice(SPRITES_JOGADOR)
        self.imagens['jogador'] = tuple(
            pygame.image.load(str(SPRITES / nome)).convert_alpha()
            for nome in sprites
        )
        self.mascaras['jogador'] = tuple(obterMascara(img) for img in self.imagens['jogador'])


    def selecionar_sprites_tubo(self):
        nome = random.choice(TUBOS)
        img_tubo = pygame.image.load(str(SPRITES / nome)).convert_alpha()
        self.imagens['tubo'] = (
            pygame.transform.flip(img_tubo, False, True),
            img_tubo,
        )
        self.mascaras['tubo'] = (
            obterMascara(self.imagens['tubo'][0]),
            obterMascara(self.imagens['tubo'][1]),
        )


    def aleatorizar(self):
        self.selecionar_fundo()
        self.selecionar_sprites_jogador()
        self.selecionar_sprites_tubo()
