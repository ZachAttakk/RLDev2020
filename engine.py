'''Engine file'''
import tcod as libtcod
import pygame
import spritesheet

import config
from entity import Entity
from map_objects.game_map import GameMap
from event_handlers import handle_events
from render_functions import render_entities, render_map

# Grab config
CONFIG = config.Config()


def main():
    '''Main engine function'''

    # Init pygame
    pygame.init()

    # get surface size
    scale = CONFIG.Game.get("scale")
    # make main surface
    pygame.display.set_mode(
        size=(int(CONFIG.Game["game_width"] * scale), int(CONFIG.Game["game_height"] * scale)))

    # preload sprite sheets
    spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)
    # make player and rando NPC
    # TODO: Magic numbers!
    PLAYER = Entity(spritesheets.get(CONFIG.Sprites.get("player").get(
        "sheet")).sprite_at(CONFIG.Sprites.get("player").get("values")), (7, 5))
    npc = Entity(spritesheets.get(CONFIG.Sprites.get("npc").get(
        "sheet")).sprite_at(CONFIG.Sprites.get("npc").get("values")), (3, 3))

    ENTITIES = [PLAYER, npc]

    # Make us a map!
    GAME_MAP = GameMap(CONFIG.Game.get("map_width"),
                       CONFIG.Game.get("map_height"))

    # gobal quit flag
    should_quit = False

    # MAIN LOOP
    while not should_quit:

        # handle inputs
        messages = handle_events(pygame.event.get())

        if messages.get("move"):
            PLAYER.move(messages["move"])

        should_quit = messages.get('exit')

        # print to screen
        draw_all(ENTITIES, GAME_MAP, spritesheets)

    # ... and we're done!
    pygame.quit()


def draw_all(ENTITIES, MAP, spritesheets):
    '''Draw game window every frame'''

    # global use of SURFACE_MAIN
    surface_main = pygame.display.get_surface()

    surface_map = pygame.surface.Surface(size=(CONFIG.Game.get(
        "game_width"), CONFIG.Game.get("game_height")), flags=surface_main.get_flags()).convert_alpha()

    # clear screen
    surface_main.fill(tuple(CONFIG.Colors.get("black")))

    # draw map
    render_map(surface_map, MAP, spritesheets,
               CONFIG.Sprites, CONFIG.Game.get("tile_size"))

    # draw entities
    render_entities(surface_map, ENTITIES, CONFIG.Game.get("tile_size"))

    # Now we scale up and blit to the screen.
    _scale = CONFIG.Game.get("scale")
    if _scale != 1.0:
        _scaled_size = list(surface_map.get_size())
        _scaled_size = [int(i * _scale) for i in _scaled_size]
        pygame.transform.scale(surface_map, tuple(
            _scaled_size), surface_main).convert_alpha()
    else:
        surface_main.blit(surface_map, (0, 0))
    # Push to screen
    pygame.display.flip()


# MAKE IT SO
if __name__ == '__main__':
    main()
