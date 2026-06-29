import pygame

from src.config import BASE_Y


def getHitmask(image):
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return False
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def checkCrash(px, py, player_index, upper_pipes, lower_pipes, rm):
    player_h = rm.images['player'][0].get_height()
    player_w = rm.images['player'][0].get_width()
    if py + player_h >= BASE_Y - 1:
        return (True, True)
    player_rect = pygame.Rect(px, py, player_w, player_h)
    pipe_w = rm.images['pipe'][0].get_width()
    pipe_h = rm.images['pipe'][0].get_height()
    for uPipe, lPipe in zip(upper_pipes, lower_pipes):
        u_rect = pygame.Rect(uPipe['x'], uPipe['y'], pipe_w, pipe_h)
        l_rect = pygame.Rect(lPipe['x'], lPipe['y'], pipe_w, pipe_h)
        u_collide = pixelCollision(player_rect, u_rect,
                                   rm.hitmasks['player'][player_index],
                                   rm.hitmasks['pipe'][0])
        l_collide = pixelCollision(player_rect, l_rect,
                                   rm.hitmasks['player'][player_index],
                                   rm.hitmasks['pipe'][1])
        if u_collide or l_collide:
            return (True, False)
    return (False, False)
