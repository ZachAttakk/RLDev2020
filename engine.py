'''Engine file'''
import tcod as libtcod
import pygame

import config
from entity import Entity
from event_handlers import handle_events
from render_functions import render_entities


# GLOBAL VARIABLES
CONFIG = config.Config()
ENTITIES = []
PLAYER = Entity()


def main():
    '''Main engine function'''

    # gobal quit flag
    should_quit = False

    # main loop
    while not should_quit:

        # handle inputs
        messages = handle_events(pygame.event.get())

        if messages.get("move"):
            PLAYER.move(messages["move"])

        should_quit = messages.get('exit')
        # print to screen
        draw()

    # ... and we're done!
    pygame.quit()


def initialize():
    ''' ONLY TO BE RUN ON INITIAL START! This is not a restart!'''
    # We'll be referencing the global SURFACE_MAIN
    global ENTITIES
    global PLAYER

    # Init pygame
    pygame.init()

    # make player and rando NPC
    # TODO: Magic numbers!
    PLAYER = Entity((7, 5), CONFIG.SpriteSheets.get(
        "char"), CONFIG.Sprites["player"])
    npc = Entity((3, 3), CONFIG.SpriteSheets.get(
        "char"), CONFIG.Sprites["npc"])

    ENTITIES = [PLAYER, npc]

    # get surface size
    scale = CONFIG.Game.get("scale")
    # make main surface
    pygame.display.set_mode(
        size=(int(CONFIG.Game["game_width"] * scale), int(CONFIG.Game["game_height"] * scale)))


def draw():
    '''Draw game window every frame'''
    # global use of SURFACE_MAIN
    surface_main = pygame.display.get_surface()

    surface_map = pygame.surface.Surface(size=(CONFIG.Game.get(
        "game_width"), CONFIG.Game.get("game_height")), flags=surface_main.get_flags())
    # clear screen
    surface_main.fill(tuple(CONFIG.Colors["black"]))
    # TODO draw map

    render_entities(surface_map, ENTITIES, CONFIG.Game.get(
        "tile_size"), CONFIG.Game.get("tile_gap"))

    # Now we scale up and blit to the screen.
    if CONFIG.Game.get("scale") > 1.0:
        pygame.transform.scale2x(surface_map, surface_main)
    else:
        surface_main.blit(surface_map, (0, 0))
    # Push to screen
    pygame.display.flip()


# MAKE IT SO
if __name__ == '__main__':
    initialize()
    main()
