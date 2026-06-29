import sys

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ICON, BASE_Y
from src.engine.resource_manager import ResourceManager
from src.states.state_machine import StateMachine
from src.states.welcome_state import WelcomeState


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        icon = pygame.image.load(str(ICON))
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.rm = ResourceManager()
        self.rm.load()
        self.sm = StateMachine()

    def run(self):
        self.sm.change(WelcomeState(self))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._quit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    self._quit()
                self.sm.handle_event(event)
            self.sm.update()
            self.sm.render(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def _quit(self):
        pygame.quit()
        sys.exit()
