import pygame
MOVE_KEYS = {
    # Arrow keys.
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_HOME: (-1, -1),
    pygame.K_END: (-1, 1),
    pygame.K_PAGEUP: (1, -1),
    pygame.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    pygame.K_KP1: (-1, 1),
    pygame.K_KP2: (0, 1),
    pygame.K_KP3: (1, 1),
    pygame.K_KP4: (-1, 0),
    pygame.K_KP6: (1, 0),
    pygame.K_KP7: (-1, -1),
    pygame.K_KP8: (0, -1),
    pygame.K_KP9: (1, -1),
    # Vi keys, but only works on QWERTY
    pygame.K_h: (-1, 0),
    pygame.K_j: (0, 1),
    pygame.K_k: (0, -1),
    pygame.K_l: (1, 0),
    pygame.K_y: (-1, -1),
    pygame.K_u: (1, -1),
    pygame.K_b: (-1, 1),
    pygame.K_n: (1, 1),
}

WAIT_KEYS = {
    pygame.K_PERIOD,
    pygame.K_KP5,
    pygame.K_CLEAR,
}
