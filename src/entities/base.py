from src.config import BASE_Y


class Base:
    def __init__(self, rm):
        self.rm = rm
        self.x = 0
        self._shift = rm.images['base'].get_width() - rm.images['background'].get_width()

    def reset(self):
        self.x = 0

    def update(self, speed=100):
        self.x = -((-self.x + speed) % self._shift)

    def draw(self, screen):
        screen.blit(self.rm.images['base'], (self.x, BASE_Y))
