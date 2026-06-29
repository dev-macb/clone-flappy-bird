import pygame
from pygame.locals import KEYDOWN, K_SPACE, K_UP

from src.config import SCREEN_WIDTH, BASE_Y
from src.states.state_machine import State
from src.systems.score import render_score


class GameOverState(State):
    def enter(self, **kwargs):
        self.rm = self.game.rm
        self.score = kwargs['score']
        self.player_x = SCREEN_WIDTH * 0.2
        self.player_y = kwargs['y']
        self.player_h = self.rm.images['player'][0].get_height()
        self.player_vel_y = kwargs['player_vel_y']
        self.player_acc_y = 2
        self.player_rot = kwargs['player_rot']
        self.player_vel_rot = 7
        self.basex = kwargs['basex']
        self.upper_pipes = kwargs['upper_pipes']
        self.lower_pipes = kwargs['lower_pipes']
        self.ground_crash = kwargs['ground_crash']
        self.rm.sounds['hit'].play()
        if not self.ground_crash:
            self.rm.sounds['die'].play()

    def handle_event(self, event):
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            if self.player_y + self.player_h >= BASE_Y - 1:
                from src.states.welcome_state import WelcomeState
                self.game.sm.change(WelcomeState(self.game))

    def update(self):
        if self.player_y + self.player_h < BASE_Y - 1:
            self.player_y += min(self.player_vel_y, BASE_Y - self.player_y - self.player_h)
        if self.player_vel_y < 15:
            self.player_vel_y += self.player_acc_y
        if not self.ground_crash and self.player_rot > -90:
            self.player_rot -= self.player_vel_rot

    def render(self, screen):
        screen.blit(self.rm.images['background'], (0, 0))
        for uPipe, lPipe in zip(self.upper_pipes, self.lower_pipes):
            screen.blit(self.rm.images['pipe'][0], (uPipe['x'], uPipe['y']))
            screen.blit(self.rm.images['pipe'][1], (lPipe['x'], lPipe['y']))
        screen.blit(self.rm.images['base'], (self.basex, BASE_Y))
        render_score(screen, self.score, self.rm)
        player_surface = pygame.transform.rotate(self.rm.images['player'][1], self.player_rot)
        screen.blit(player_surface, (self.player_x, self.player_y))
        screen.blit(self.rm.images['gameover'], (50, 180))
