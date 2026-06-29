from itertools import cycle

import pygame
from pygame.locals import KEYDOWN, K_SPACE, K_UP

from src.config import SCREEN_WIDTH, BASE_Y
from src.entities.base import Base
from src.entities.pipe import get_random_pipe_pair
from src.states.state_machine import State
from src.systems.collision import checkCrash
from src.systems.score import render_score


class PlayState(State):
    def enter(self, **kwargs):
        self.rm = self.game.rm
        self.score = 0
        self.player_index = 0
        self.loop_iter = 0
        self.player_index_gen = kwargs.get('player_index_gen', cycle([0, 1, 2, 1]))
        self.player_x = int(SCREEN_WIDTH * 0.2)
        self.player_y = kwargs['playery']
        self.base = Base(self.rm)
        self.base.x = kwargs['basex']
        upper1, lower1 = get_random_pipe_pair(self.rm)
        upper2, lower2 = get_random_pipe_pair(self.rm)
        self.upper_pipes = [
            {'x': SCREEN_WIDTH + 200, 'y': upper1['y']},
            {'x': SCREEN_WIDTH + 200 + SCREEN_WIDTH / 2, 'y': upper2['y']},
        ]
        self.lower_pipes = [
            {'x': SCREEN_WIDTH + 200, 'y': lower1['y']},
            {'x': SCREEN_WIDTH + 200 + SCREEN_WIDTH / 2, 'y': lower2['y']},
        ]
        self.player_vel_y = -9
        self.player_max_vel_y = 10
        self.player_acc_y = 1
        self.player_rot = 45
        self.player_vel_rot = 3
        self.player_rot_thr = 20
        self.player_flap_acc = -9
        self.player_flapped = False

    def handle_event(self, event):
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            if self.player_y > -2 * self.rm.images['player'][0].get_height():
                self.player_vel_y = self.player_flap_acc
                self.player_flapped = True
                self.rm.sounds['wing'].play()

    def update(self):
        crash = checkCrash(self.player_x, self.player_y, self.player_index,
                           self.upper_pipes, self.lower_pipes, self.rm)
        if crash[0]:
            from src.states.gameover_state import GameOverState
            self.game.sm.change(
                GameOverState(self.game),
                y=self.player_y, ground_crash=crash[1],
                basex=self.base.x, upper_pipes=self.upper_pipes,
                lower_pipes=self.lower_pipes, score=self.score,
                player_vel_y=self.player_vel_y, player_rot=self.player_rot,
            )
            return
        player_mid = self.player_x + self.rm.images['player'][0].get_width() / 2
        for pipe in self.upper_pipes:
            pipe_mid = pipe['x'] + self.rm.images['pipe'][0].get_width() / 2
            if pipe_mid <= player_mid < pipe_mid + 4:
                self.score += 1
                self.rm.sounds['point'].play()
        if (self.loop_iter + 1) % 3 == 0:
            self.player_index = next(self.player_index_gen)
        self.loop_iter = (self.loop_iter + 1) % 30
        self.base.update()
        if self.player_rot > -90:
            self.player_rot -= self.player_vel_rot
        if self.player_vel_y < self.player_max_vel_y and not self.player_flapped:
            self.player_vel_y += self.player_acc_y
        if self.player_flapped:
            self.player_flapped = False
            self.player_rot = 45
        player_h = self.rm.images['player'][self.player_index].get_height()
        self.player_y += min(self.player_vel_y, BASE_Y - self.player_y - player_h)
        for uPipe, lPipe in zip(self.upper_pipes, self.lower_pipes):
            uPipe['x'] -= 4
            lPipe['x'] -= 4
        if len(self.upper_pipes) > 0 and 0 < self.upper_pipes[0]['x'] < 5:
            upper, lower = get_random_pipe_pair(self.rm)
            self.upper_pipes.append(upper)
            self.lower_pipes.append(lower)
        pipe_w = self.rm.images['pipe'][0].get_width()
        if len(self.upper_pipes) > 0 and self.upper_pipes[0]['x'] < -pipe_w:
            self.upper_pipes.pop(0)
            self.lower_pipes.pop(0)

    def render(self, screen):
        screen.blit(self.rm.images['background'], (0, 0))
        for uPipe, lPipe in zip(self.upper_pipes, self.lower_pipes):
            screen.blit(self.rm.images['pipe'][0], (uPipe['x'], uPipe['y']))
            screen.blit(self.rm.images['pipe'][1], (lPipe['x'], lPipe['y']))
        self.base.draw(screen)
        render_score(screen, self.score, self.rm)
        visible_rot = self.player_rot_thr
        if self.player_rot <= self.player_rot_thr:
            visible_rot = self.player_rot
        player_surface = pygame.transform.rotate(
            self.rm.images['player'][self.player_index], visible_rot)
        screen.blit(player_surface, (self.player_x, self.player_y))
