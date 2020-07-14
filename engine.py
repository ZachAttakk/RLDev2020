'''Engine file'''
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Iterable
import numpy as np
from tcod.map import compute_fov
import pygame
import spritesheet

from config import Config as CONFIG
from entity import Entity
from map_objects.game_map import GameMap
from message_log import MessageLog
import event_handlers
import render_functions

if TYPE_CHECKING:
    from entity import Entity
    from map_objects.game_map import GameMap


class Engine:
    """Vanilla engine class"""

    game_map: GameMap

    def __init__(self, player: Actor):
        self.PLAYER = player
        self.spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)
        self.fonts = self.load_fonts(CONFIG.Fonts)
        self.message_log = MessageLog()
        self.eventhandler: event_handlers.EventHandler = event_handlers.MainGameEventHandler(
            self)

    @staticmethod
    def load_fonts(fonts):
        loaded_fonts = {}
        for i in fonts:
            # for each font in the list, grab the dictionary under it
            _ff = fonts.get(i)
            # make a font from it, add it to the dictionary that's being returned
            loaded_fonts[i] = pygame.font.Font(_ff.get("path"), 8)
            # and send them back
        return loaded_fonts

    def handle_enemy_turns(self) -> None:
        for entity in set(self.GAMEMAP.actors) - {self.PLAYER}:
            if entity.ai:
                entity.ai.perform()

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

        # for the time being the map will always be square and the whole thing will show
        surface_map = pygame.surface.Surface(
            size=(CONFIG.Display.get("game_height"),
                  CONFIG.Display.get("game_height")),
            flags=surface_main.get_flags()).convert_alpha()

        # clear screen
        surface_map.fill(CONFIG.get_colour("black"))

        # draw map
        render_functions.render_map(surface_map, self.GAMEMAP, self.spritesheets,
                                    CONFIG.Sprites, CONFIG.Display.get("tile_size"))

        # log will take up the rest of the space on the right
        log_size = (
            int(CONFIG.Display.get("game_width") - CONFIG.Display.get("game_height")),
            CONFIG.Display.get("game_height"))

        surface_log = self.message_log.render_messages(
            size=log_size, messages=self.message_log.messages, font=self.fonts.get("mini"))

        render_functions.render_bar(surface_map, current_value=self.PLAYER.fighter.hp,
                                    max_value=self.PLAYER.fighter.max_hp, total_width=60, font=self.fonts.get("mini"))

        # MAKE SURE THIS IS ALWAYS LAST IN RENDER ORDER
        # render scanlines if there should be any
        if CONFIG.Display.get("scanline_opacity") not in [0, None]:
            render_functions.render_scanlines(surface_map)

        # Now we blit to the screen.

        surface_main.blit(surface_map, (0, 0))
        # to the right of the map
        surface_main.blit(surface_log, (surface_map.get_width(), 0))

        # Push to screen
        pygame.display.flip()
