from itertools import cycle

import pygame

from src.config import PLAYER_X, PLAYER_FLAP_ACC, PLAYER_MAX_VEL_Y, PLAYER_ACC_Y, BASE_Y


class Player:
    def __init__(self, rm, y=0):
        self.rm = rm
        self.x = PLAYER_X
        self.y = y
        self.vel_y = -9
        self.rot = 45
        self.index = 0
        self.index_gen = cycle([0, 1, 2, 1])
        self.loop_iter = 0
        self.flapped = False

    def flap(self):
        if self.y > -2 * self.rm.images['player'][0].get_height():
            self.vel_y = PLAYER_FLAP_ACC
            self.flapped = True

    def update(self):
        if (self.loop_iter + 1) % 3 == 0:
            self.index = next(self.index_gen)
        self.loop_iter = (self.loop_iter + 1) % 30
        if self.rot > -90:
            self.rot -= 3
        if self.vel_y < PLAYER_MAX_VEL_Y and not self.flapped:
            self.vel_y += PLAYER_ACC_Y
        if self.flapped:
            self.flapped = False
            self.rot = 45
        player_h = self.rm.images['player'][self.index].get_height()
        self.y += min(self.vel_y, BASE_Y - self.y - player_h)

    def get_visible_rot(self):
        return min(self.rot, 20)

    def draw(self, screen):
        visible_rot = self.get_visible_rot()
        surface = pygame.transform.rotate(self.rm.images['player'][self.index], visible_rot)
        screen.blit(surface, (self.x, self.y))
