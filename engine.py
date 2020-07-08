'''Engine file'''
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Iterable
from tcod.map import compute_fov
import pygame
import spritesheet

from config import Config as CONFIG
from entity import Entity
from map_objects.game_map import GameMap
import event_handlers
import render_functions

if TYPE_CHECKING:
    from entity import Entity
    from map_objects.game_map import GameMap


class Engine:
    """Vanilla engine class"""

    game_map: GameMap

    def __init__(self, player: Entity):
        self.PLAYER = player
        self.spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)
        self.eventhandler: event_handlers.EventHandler = event_handlers.EventHandler(
            self)

    def handle_enemy_turns(self) -> None:
        for entity in self.GAMEMAP.entities - {self.PLAYER}:
            print(f"The {entity.name} wanted to do a thing, but it forgot.")

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view."""

        # TODO: Magic numbers!
        self.GAMEMAP.visible[:] = compute_fov(
            self.GAMEMAP.tiles["transparent"], self.PLAYER.position,
            radius=CONFIG.Game.get("fov_radius")
        )
        # if a tile is visible it should be added to explored
        self.GAMEMAP.explored |= self.GAMEMAP.visible

    def render(self, console):
        '''Draw game window every frame'''

        # global use of SURFACE_MAIN
        surface_main = console

        surface_map = pygame.surface.Surface(
            size=(CONFIG.Display.get("game_width"),
                  CONFIG.Display.get("game_height")),
            flags=surface_main.get_flags()).convert_alpha()

        # clear screen
        surface_map.fill(tuple(CONFIG.Colours.get("black")))

        # draw map
        render_functions.render_map(surface_map, self.GAMEMAP, self.spritesheets,
                                    CONFIG.Sprites, CONFIG.Display.get("tile_size"))

        # render scanlines if there should be any
        if CONFIG.Display.get("scanline_opacity") not in [0, None]:
            render_functions.render_scanlines(surface_map)

        # Now we scale up and blit to the screen.
        _scale = CONFIG.Display.get("scale")
        if _scale != 1.0:
            _scaled_size = list(surface_map.get_size())
            _scaled_size = [int(i * _scale) for i in _scaled_size]
            pygame.transform.scale(surface_map, tuple(
                _scaled_size), surface_main).convert_alpha()
        else:
            surface_main.blit(surface_map, (0, 0))
        # Push to screen
        pygame.display.flip()
