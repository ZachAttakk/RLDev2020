'''Engine file'''
import tcod as libtcod
import pygame

import config
import spritesheet
from event_handlers import handle_events


# GLOBAL VARIABLES
SURFACE_MAIN = None
CONFIG = config.Config()


def main():
    '''Main engine function'''

    # gobal quit flag
    should_quit = False

    # main loop
    while not should_quit:

        # handle inputs
        messages = handle_events(pygame.event.get())
        should_quit = messages.get('exit')
        # print to screen
        draw()

    # ... and we're done!
    pygame.quit()


def initialize():
    ''' ONLY TO BE RUN ON INITIAL START! This is not a restart (yet)!'''
    # We'll be referencing the global SURFACE_MAIN
    global SURFACE_MAIN

    # Init pygame
    pygame.init()

    # make main surface
    SURFACE_MAIN = pygame.display.set_mode(
        size=(int(CONFIG.Game["game_width"]), int(CONFIG.Game["game_height"])))


def draw():
    '''Draw game window every frame'''
    # global use of SURFACE_MAIN
    global SURFACE_MAIN

    # clear screen
    SURFACE_MAIN.fill(tuple(CONFIG.Colors["black"]))
    # TODO draw map
    # draw character
    # player = pygame.image.load(os.path.join("tiles", CONFIG.Sprites.player.value))
    ss = spritesheet.spritesheet(
        CONFIG.SpriteSheets["char"], CONFIG.Game["tile_size"], CONFIG.Game["tile_gap"])

    image = ss.sprite_at(tuple(CONFIG.Sprites["player"]))
    SURFACE_MAIN.blit(image, (200, 200))

    # Push to screen
    pygame.display.flip()


# MAKE IT SO
if __name__ == '__main__':
    initialize()
    main()
