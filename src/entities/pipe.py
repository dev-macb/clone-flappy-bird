import random

from src.config import SCREEN_WIDTH, BASE_Y, PIPE_GAP_SIZE


def get_random_pipe_pair(rm):
    gap_y = random.randrange(0, int(BASE_Y * 0.6 - PIPE_GAP_SIZE))
    gap_y += int(BASE_Y * 0.2)
    pipe_h = rm.images['pipe'][0].get_height()
    pipe_x = SCREEN_WIDTH + 10
    return (
        {'x': pipe_x, 'y': gap_y - pipe_h},
        {'x': pipe_x, 'y': gap_y + PIPE_GAP_SIZE},
    )
