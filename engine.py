'''Engine file'''
from typing import Set, Iterable
from tcod.map import compute_fov
import pygame
import spritesheet

from config import Config
from entity import Entity
from map_objects.game_map import GameMap
import event_handlers
from render_functions import render_entities, render_map


class Engine:
    def __init__(self, entities: Set[Entity], game_map: GameMap, player: Entity, config: Config = None):
        self.ENTITIES = entities
        self.GAMEMAP = game_map
        self.PLAYER = player
        self.CONFIG = config
        self.spritesheets = spritesheet.get_sheets(config.SpriteSheets)
        self.update_fov()

    def handle_events(self, events: Iterable[pygame.event.EventType]):
        for event in events:
            action = event_handlers.handle_event(event)
            if action is None:
                continue
            # do the thing.
            # actions will handle their own validation
            action.perform(self, self.PLAYER)

            # update FOV
            self.update_fov()

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view."""

        # TODO: Magic numbers!
        self.GAMEMAP.visible[:] = compute_fov(
            self.GAMEMAP.tiles["transparent"], self.PLAYER.position, radius=8
        )
        # if a tile is visible it should be added to explored
        self.GAMEMAP.explored |= self.GAMEMAP.visible

    def render(self, console):
        '''Draw game window every frame'''

        # global use of SURFACE_MAIN
        surface_main = console

        surface_map = pygame.surface.Surface(
            size=(self.CONFIG.Game.get("game_width"),
                  self.CONFIG.Game.get("game_height")),
            flags=surface_main.get_flags()).convert_alpha()

        # clear screen
        surface_main.fill(tuple(self.CONFIG.Colors.get("black")))

        # draw map
        render_map(surface_map, self.GAMEMAP, self.spritesheets,
                   self.CONFIG.Sprites, self.CONFIG.Game.get("tile_size"))

        # draw entities
        render_entities(surface_map, self.ENTITIES,
                        self.CONFIG.Game.get("tile_size"))

        # Now we scale up and blit to the screen.
        _scale = self.CONFIG.Game.get("scale")
        if _scale != 1.0:
            _scaled_size = list(surface_map.get_size())
            _scaled_size = [int(i * _scale) for i in _scaled_size]
            pygame.transform.scale(surface_map, tuple(
                _scaled_size), surface_main).convert_alpha()
        else:
            surface_main.blit(surface_map, (0, 0))
        # Push to screen
        pygame.display.flip()
