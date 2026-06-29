from itertools import cycle

from pygame.locals import KEYDOWN, K_SPACE, K_UP

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.entities.base import Base
from src.states.state_machine import State


class WelcomeState(State):
    def enter(self, **kwargs):
        self.rm = self.game.rm
        self.rm.randomize()
        self.player_index = 0
        self.player_index_gen = cycle([0, 1, 2, 1])
        self.loop_iter = 0
        self.player_x = int(SCREEN_WIDTH * 0.2)
        self.player_y = int((SCREEN_HEIGHT - self.rm.images['player'][0].get_height()) / 2)
        self.message_x = int((SCREEN_WIDTH - self.rm.images['message'].get_width()) / 2)
        self.message_y = int(SCREEN_HEIGHT * 0.12)
        self.base = Base(self.rm)
        self.base.reset()
        self.shm_val = 0
        self.shm_dir = 1

    def handle_event(self, event):
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            self.rm.sounds['wing'].play()
            from src.states.play_state import PlayState
            self.game.sm.change(
                PlayState(self.game),
                playery=self.player_y + self.shm_val,
                basex=self.base.x,
                player_index_gen=self.player_index_gen,
            )

    def update(self):
        if (self.loop_iter + 1) % 5 == 0:
            self.player_index = next(self.player_index_gen)
        self.loop_iter = (self.loop_iter + 1) % 30
        self.base.update()
        if abs(self.shm_val) == 8:
            self.shm_dir *= -1
        self.shm_val += self.shm_dir

    def render(self, screen):
        screen.blit(self.rm.images['background'], (0, 0))
        screen.blit(self.rm.images['player'][self.player_index],
                    (self.player_x, self.player_y + self.shm_val))
        screen.blit(self.rm.images['message'], (self.message_x, self.message_y))
        self.base.draw(screen)
