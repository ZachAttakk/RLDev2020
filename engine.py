'''''Engine file'''''
import os
import tcod as libtcod
import pygame

import config
import spritesheet
from event_handlers import handle_events


# GLOBAL VARIABLES
SURFACE_MAIN = None


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
        size=(int(config.Game.game_width.value), int(config.Game.game_height.value)))


def draw():
    '''Draw game window every frame'''
    # global use of SURFACE_MAIN
    global SURFACE_MAIN

    # clear screen
    SURFACE_MAIN.fill(config.Colors.black.value)
    # TODO draw map
    # draw character
    # player = pygame.image.load(os.path.join("tiles", config.Sprites.player.value))
    ss = spritesheet.spritesheet(
        config.SpriteSheets.base.value, config.Game.tile_size.value, config.Game.tile_gap.value)
    # Sprite is 16x16 pixels at location 0,0 in the file...
    image = ss.sprite_at(config.Sprites.player.value)
    SURFACE_MAIN.blit(image, (200, 200))
    # Push to screen
    pygame.display.flip()


# MAKE IT SO
if __name__ == '__main__':
    initialize()
    main()
