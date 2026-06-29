from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ATIVOS = RAIZ / 'assets'
SPRITES = ATIVOS / 'sprites'
AUDIO = ATIVOS / 'audio'
ICONE = ATIVOS / 'flappy.ico'

FPS = 30
LARGURA_TELA = 288
ALTURA_TELA = 512
Y_CHAO = ALTURA_TELA * 0.79
TAMANHO_VAO_TUBO = 100

JOGADOR_X = int(LARGURA_TELA * 0.2)
JOGADOR_VEL_Y_MAXIMO = 10
JOGADOR_VEL_Y_MINIMO = -8
JOGADOR_ACEL_Y = 1
JOGADOR_ACEL_BATIDA = -9
JOGADOR_LIMIAR_ROT = 20
JOGADOR_VEL_ROT = 3

VEL_X_TUBO = -4

SPRITES_JOGADOR = (
    ('redbird-upflap.png', 'redbird-midflap.png', 'redbird-downflap.png'),
    ('bluebird-upflap.png', 'bluebird-midflap.png', 'bluebird-downflap.png'),
    ('yellowbird-upflap.png', 'yellowbird-midflap.png', 'yellowbird-downflap.png'),
)

FUNDOS = ('background-day.png', 'background-night.png')

TUBOS = ('pipe-green.png', 'pipe-red.png')

NUMEROS = tuple(f'{i}.png' for i in range(10))

SPRITE_FIM_DE_JOGO = 'gameover.png'
SPRITE_MENSAGEM = 'message.png'
SPRITE_CHAO = 'base.png'
