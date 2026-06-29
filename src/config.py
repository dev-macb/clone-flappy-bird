from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / 'assets'
SPRITES = ASSETS / 'sprites'
AUDIO = ASSETS / 'audio'
ICON = ASSETS / 'flappy.ico'

FPS = 30
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
BASE_Y = SCREEN_HEIGHT * 0.79
PIPE_GAP_SIZE = 100

PLAYER_X = int(SCREEN_WIDTH * 0.2)
PLAYER_MAX_VEL_Y = 10
PLAYER_MIN_VEL_Y = -8
PLAYER_ACC_Y = 1
PLAYER_FLAP_ACC = -9
PLAYER_ROT_THR = 20
PLAYER_ROT_VEL = 3

PIPE_VEL_X = -4

PLAYER_SPRITES = (
    ('redbird-upflap.png', 'redbird-midflap.png', 'redbird-downflap.png'),
    ('bluebird-upflap.png', 'bluebird-midflap.png', 'bluebird-downflap.png'),
    ('yellowbird-upflap.png', 'yellowbird-midflap.png', 'yellowbird-downflap.png'),
)

BACKGROUNDS = ('background-day.png', 'background-night.png')

PIPES = ('pipe-green.png', 'pipe-red.png')

NUMBERS = tuple(f'{i}.png' for i in range(10))

GAMEOVER_SPRITE = 'gameover.png'
MESSAGE_SPRITE = 'message.png'
BASE_SPRITE = 'base.png'
