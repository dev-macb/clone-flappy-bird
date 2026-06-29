import sys
import random

import pygame

from src.config import (
    SPRITES, AUDIO, BACKGROUNDS, PLAYER_SPRITES,
    PIPES, NUMBERS, GAMEOVER_SPRITE, MESSAGE_SPRITE, BASE_SPRITE,
)
from src.systems.collision import getHitmask


class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.hitmasks = {}
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        self._loaded = True
        self._load_numbers()
        self._load_statics()
        self._load_sounds()

    def _load_numbers(self):
        self.images['numbers'] = tuple(
            pygame.image.load(str(SPRITES / name)).convert_alpha()
            for name in NUMBERS
        )

    def _load_statics(self):
        self.images['gameover'] = pygame.image.load(str(SPRITES / GAMEOVER_SPRITE)).convert_alpha()
        self.images['message'] = pygame.image.load(str(SPRITES / MESSAGE_SPRITE)).convert_alpha()
        self.images['base'] = pygame.image.load(str(SPRITES / BASE_SPRITE)).convert_alpha()

    def _load_sounds(self):
        ext = '.wav' if 'win' in sys.platform else '.ogg'
        for name in ('die', 'hit', 'point', 'swoosh', 'wing'):
            self.sounds[name] = pygame.mixer.Sound(str(AUDIO / f'{name}{ext}'))

    def select_background(self):
        name = random.choice(BACKGROUNDS)
        self.images['background'] = pygame.image.load(str(SPRITES / name)).convert()

    def select_player_sprites(self):
        sprites = random.choice(PLAYER_SPRITES)
        self.images['player'] = tuple(
            pygame.image.load(str(SPRITES / name)).convert_alpha()
            for name in sprites
        )
        self.hitmasks['player'] = tuple(getHitmask(img) for img in self.images['player'])

    def select_pipe_sprites(self):
        name = random.choice(PIPES)
        pipe_img = pygame.image.load(str(SPRITES / name)).convert_alpha()
        self.images['pipe'] = (
            pygame.transform.flip(pipe_img, False, True),
            pipe_img,
        )
        self.hitmasks['pipe'] = (
            getHitmask(self.images['pipe'][0]),
            getHitmask(self.images['pipe'][1]),
        )

    def randomize(self):
        self.select_background()
        self.select_player_sprites()
        self.select_pipe_sprites()
