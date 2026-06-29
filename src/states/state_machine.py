class State:
    def __init__(self, game):
        self.game = game

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass


class StateMachine:
    def __init__(self):
        self._states = []

    @property
    def current(self):
        return self._states[-1] if self._states else None

    def change(self, state_cls, **kwargs):
        if self._states:
            self._states[-1].exit()
        self._states = [state_cls]
        self._states[-1].enter(**kwargs)

    def handle_event(self, event):
        if self.current:
            self.current.handle_event(event)

    def update(self):
        if self.current:
            self.current.update()

    def render(self, screen):
        if self.current:
            self.current.render(screen)
