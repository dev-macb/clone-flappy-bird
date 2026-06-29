from src.config import SCREEN_WIDTH, SCREEN_HEIGHT


def render_score(screen, score, rm):
    digits = [int(x) for x in str(score)]
    total_w = sum(rm.images['numbers'][d].get_width() for d in digits)
    x = (SCREEN_WIDTH - total_w) / 2
    for d in digits:
        screen.blit(rm.images['numbers'][d], (x, SCREEN_HEIGHT * 0.1))
        x += rm.images['numbers'][d].get_width()
