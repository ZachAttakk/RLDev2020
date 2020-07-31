'''Engine file'''
from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Iterable
import numpy as np
from pygame import sprite
from tcod.map import compute_fov
import pygame
import pygame.surface
import spritesheet
import exceptions

from config import Config as CONFIG
from map_objects.game_map import GameMap
from message_log import MessageLog
import event_handlers
from render_functions import RenderEngine

if TYPE_CHECKING:
    from entity import Actor
    from map_objects.game_map import GameMap


class Engine:
    """Engine class"""

    GAMEMAP: GameMap

    def __init__(self, player: Actor):
        self.PLAYER = player
        self.message_log = MessageLog()
        self.eventhandler: event_handlers.EventHandler = event_handlers.MainGameEventHandler(
            self)
        self.mouse_position = (0, 0)
        self.render_engine = RenderEngine()

    def handle_enemy_turns(self) -> None:
        for entity in set(self.GAMEMAP.actors) - {self.PLAYER}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # ignore impossible actions when coming from AI

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
        self.render_engine.render_map(surface_map, self.GAMEMAP,
                                      CONFIG.Sprites, CONFIG.Display.get("tile_size"))

        # log will take up the rest of the space on the right
        ui_size = [
            int(CONFIG.Display.get("game_width") -
                CONFIG.Display.get("game_height")),
            CONFIG.Display.get("game_height")]
        surface_ui = self.render_engine.make_window(
            tuple(ui_size), CONFIG.Sprites.get("frame"))

        # TODO: Magic numbers!?
        surface_ui.blit(self.render_engine.make_message_log(
            size=(ui_size[0]-16, ui_size[1]-16), messages=self.message_log.messages), (8, 8))

        self.render_engine.render_bar(surface_map, current_value=self.PLAYER.fighter.hp,
                                      max_value=self.PLAYER.fighter.max_hp, total_width=60)

        # MAKE SURE THIS IS ALWAYS LAST IN RENDER ORDER
        # render scanlines if there should be any
        if CONFIG.Display.get("scanline_opacity") not in [0, None]:
            self.render_engine.render_scanlines(surface_map)

        # Now we blit to the screen.
        surface_main.blit(surface_map, (0, 0))
        # to the right of the map
        surface_main.blit(surface_ui, (surface_map.get_width(), 0))

        # render names of things under the mouse
        self.render_engine.render_names(
            surface_main, self.GAMEMAP, self.mouse_position)

        # Push to screen
        pygame.display.flip()
