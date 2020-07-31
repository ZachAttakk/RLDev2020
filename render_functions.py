from __future__ import annotations
from message_log import Message

from pygame import font
from components.inventory import Inventory
from typing import List, Reversible, TYPE_CHECKING
from typing import Tuple
import numpy as np

import pygame
import spritesheet
from config import Config as CONFIG
from map_objects import tile_types
from spritesheet import Spritesheet
from enum import auto, Enum

if TYPE_CHECKING:
    from map_objects.game_map import GameMap


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


class RenderEngine():

    map_offset = (0, 0)
    map_offset_old = (0, 0)

    def __init__(self) -> None:
        self.spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)
        self.fonts = self.load_fonts(CONFIG.Fonts)

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

    @staticmethod
    def draw_entity(con, entity, image, tile_size=16):
        # calculate position
        _x_pos = entity.pos[0] * tile_size
        _y_pos = entity.pos[1] * tile_size

        con.blit(image, (_x_pos, _y_pos))

    def render_map(self, con, game_map, sprites, tile_size=16):
        # create dummy surface that we can reposition to centre the player
        # this view will always be square
        inner_surface = pygame.Surface(
            (CONFIG.Game.get("map_width")*tile_size,
             CONFIG.Game.get("map_height")*tile_size)).convert_alpha()

        inner_surface.fill(CONFIG.get_colour("empty"))

        wall_sprite_data = sprites.get("wall")
        wall_sprite_image = self.spritesheets.get(wall_sprite_data.get(
            "sheet")).sprite_at(wall_sprite_data)

        floor_sprite_data = sprites.get("floor")
        floor_sprite_image = self.spritesheets.get(floor_sprite_data.get(
            "sheet")).sprite_at(floor_sprite_data)

        # now when we render the map and entities, we do so to this inner surface
        # We'll also need to grab the player position when we see it
        player_pos = (con.get_width()//2, con.get_width()//2)

        # render tiles either visible, explored, unexplored
        for y in range(game_map.height):
            for x in range(game_map.width):
                # get tile info for rendering
                tile = game_map.tiles[x][y]
                explored = game_map.explored[x][y]
                visible = game_map.visible[x][y]

                # if it's not explored, we don't show it at all
                if explored:
                    if tile == tile_types.wall:
                        self.draw_tile(inner_surface, x, y,
                                       wall_sprite_image, tile_size)
                    else:
                        self.draw_tile(inner_surface, x, y,
                                       floor_sprite_image, tile_size)
                        pass

                    # if it's not currently in LOS, we draw grey over it.
                    if not visible:
                        darken = pygame.Surface(
                            (tile_size, tile_size)).convert()
                        darken.fill(CONFIG.get_colour("black"))
                        darkness = CONFIG.Display.get("darkness_opacity") or 0
                        darken.set_alpha(darkness)
                        self.draw_tile(inner_surface, x, y, darken, tile_size)

        # Render entities on visible tiles
        entities_sorted_for_rendering = sorted(
            game_map.entities, key=lambda x: x.render_order.value
        )
        for _ent in entities_sorted_for_rendering:
            # only render if visible
            _ent_pos = list(_ent.position)
            if game_map.visible[_ent_pos[0], _ent_pos[1]]:
                # get sprite
                ent_sprite_image = self.spritesheets.get(
                    _ent.sprite.get("sheet")).sprite_at(_ent.sprite)
                self.draw_entity(inner_surface, _ent,
                                 ent_sprite_image, tile_size)
                # if this is the player, grab its position on screen
                if _ent == game_map.engine.PLAYER:
                    player_pos = (_ent_pos[0] * tile_size,
                                  _ent_pos[1]*tile_size)

        # offset map to center player, then blit to con
        # we use width in both cases because the display will remain square as much as possible
        offset = (con.get_width()//2 - player_pos[0],
                  con.get_width()//2 - player_pos[1])

        # check and save map offset
        if offset != self.map_offset:
            self.map_offset_old = self.map_offset
            self.map_offset = offset

        # TODO: Make lerp from one to other

        con.blit(inner_surface, offset)  # that 0,0 is what we need to replace

    def render_names(self, con, game_map, position, tile_size=16):
        """Renders entity names at a position on the map, at that position on the map"""

        # grab font from fonst list
        font = self.fonts.get("mini")

        # first transpose the given pixel position to map position
        _x, _y = position
        # offset values based on map pan
        _x = _x - self.map_offset[0]
        _y = _y - self.map_offset[1]
        tile_x = int(_x/tile_size)
        tile_y = int(_y/tile_size)

        # get the entities at that position
        names = game_map.get_names_at_location(tile_x, tile_y)
        if names:
            # offset name so it's not behind the mouse
            x_pos = position[0] + font.get_linesize()
            y_pos = position[1]
            self.render_outlined_text(
                con, names, (x_pos, y_pos), CONFIG.get_colour("white"), break_on_comma=True)

    def render_text(self, con, text: str, position: Tuple[int, int], fg_col, break_on_comma=False):

        font = self.fonts.get("mini")

        if break_on_comma and "," in text:
            text_lines = text.split(",")
            _longest = max(text_lines, key=len)
            _width = font.size(_longest)[0]
            text_surface = pygame.Surface(
                (_width, (font.get_linesize()*len(text_lines)))).convert_alpha()
            text_surface.fill(CONFIG.get_colour("empty"))

            y_offset = 0

            for line in text_lines:
                print_pos = (0, y_offset)
                self.render_text(
                    text_surface, line.strip(), (0, y_offset), fg_col, font)
                y_offset += font.get_linesize()
        else:
            text_surface = font.render(
                text, False, CONFIG.get_colour(fg_col))

        con.blit(text_surface, position)

    def render_outlined_text(self, con, text, position: Tuple[int, int], fg_col, break_on_comma=False):
        # 9 positions, either way of the middle

        for x in range(-1, 2):
            for y in range(-1, 2):
                temp_x, temp_y = position
                temp_x += x
                temp_y += y
                self.render_text(con, text, (temp_x, temp_y),
                                 "black", break_on_comma)

        # and the actual text...
        self.render_text(con, text, position, fg_col, break_on_comma)

    @staticmethod
    def render_scanlines(con):

        # make color with scanline opacity
        line_color = list(CONFIG.get_colour("black"))
        # if "black" provides no alpha (which is shouldn't), add it
        if len(line_color) < 4:
            line_color.append(255)
        # override any existing alpha
        line_color[3] = (CONFIG.Display.get("scanline_opacity"))
        # make surface and repeat scanline
        _lines = pygame.Surface(con.get_size()).convert_alpha()
        _lines.fill(CONFIG.get_colour("empty"))

        for i in range(0, _lines.get_height(), CONFIG.Display.get("scanline_spacing")):
            pygame.draw.line(_lines, line_color,
                             (0, i), (_lines.get_width(), i))

        con.blit(_lines, (0, 0))

    @staticmethod
    def draw_tile(con, x, y, tile, tile_size):
        _x = x * tile_size
        _y = y * tile_size
        con.blit(tile, (_x, _y))

    def render_bar(self, con, current_value, max_value, total_width) -> None:
        bar_width = int(float(current_value) / max_value * total_width)

        _bar = pygame.Surface((total_width, 10)).convert()
        _bar.fill(CONFIG.get_colour("bar_empty"))
        if bar_width > 0:
            pygame.draw.rect(_bar, CONFIG.get_colour(
                "bar_filled"), pygame.Rect(0, 0, bar_width, 10))
        self.render_text(_bar, f"HP: {current_value}/{max_value}", (1, 0), CONFIG.get_colour(
            "white"))

        con.blit(_bar, (0, 0))

    # def render_enventory(con, inventory: Inventory):

    def make_window(self, size, decorations, tile_size=16):
        """Create a window that can be displayed

        Args:
            size (Tuple(int,int)): Size of window in x and y
            sheets : [description]
            decorations (dict): Configc entry with sprite details for window decorations

        Returns:
            Surface: The window containing decorations and background
        """
        # get needed data
        # this should be 9 sprites in a list
        # 0 111111 2
        # 3        5
        # 3        5
        # 6 777777 8
        _sheet = self.spritesheets.get(decorations.get("sheet"))
        _sprites = _sheet.sprites_at(decorations)
        # create surface
        window = pygame.Surface(size).convert_alpha()
        # apply background colour
        if decorations.get("bgcolour"):
            window.fill(CONFIG.get_colour(decorations.get("bgcolour")))
        # place side lengths
        # leave the corners
        for i in range(tile_size, size[1]-tile_size, tile_size):
            window.blit(_sprites[3], (0, i))
            window.blit(_sprites[5], (size[0]-tile_size, i))

        for i in range(tile_size, size[1]-tile_size, tile_size):
            window.blit(_sprites[1], (i, 0))
            window.blit(_sprites[7], (i, size[1]-tile_size))
        # place 4 corner pieces
        window.blit(_sprites[0], (0, 0))
        window.blit(_sprites[2], (size[0]-tile_size, 0))
        window.blit(_sprites[6], (0, size[1]-tile_size))
        window.blit(_sprites[8], (size[0]-tile_size, size[1]-tile_size))

        # return surface
        return window

    def make_message_log(self, size: Tuple[int, int],
                         messages: Reversible[Message]) -> None:
        """Render the messages provided and return them on a surface
        """
        font = self.fonts.get("mini")

        con = pygame.Surface(size).convert_alpha()
        con.fill(CONFIG.get_colour("empty"))
        # start the first one 2 pixels off the bottom
        y_offset = size[1] - font.get_linesize()

        for message in reversed(messages):
            for line in reversed(self.wrap_text(message.full_text, int(size[0]))):
                print_pos = (0, y_offset)
                self.render_text(
                    con, line, print_pos, message.fg_col)
                y_offset -= font.get_linesize()

            if y_offset < 0:
                break  # log is full

        return con

    def wrap_text(self, text, width):
        """Returns list of strings that all fit within pixel width using given font"""
        results = []

        seperator = " "

        _split_words = text.split()

        font = self.fonts.get("mini")

        # Quick check if the whole string fits
        # (also removes extra whitespace)
        _check = seperator.join(_split_words)
        if font.size(_check)[0] <= width:
            return [text, ]

        # do this until we're out of words
        while len(_split_words) > 0:
            # temporary variable with the last result that fit
            _last_fit = ""
            for i in range(1, len(_split_words)+1):
                # make line with one more word than last time
                _check = seperator.join(_split_words[:i])
                # check if it's too long, in which case we store the last one that fit
                if (font.size(_check)[0] > width):
                    # add last fit
                    results.append(_last_fit)
                    # remove those from the list
                    _split_words = _split_words[i-1:]
                    # kill the loop so we can start over
                    break
                elif i == len(_split_words):
                    # this was the last iteration
                    # if it reaches here, we know the remaining part is short enough
                    results.append(_check)
                    # still remove the part we stored
                    _split_words = _split_words[i:]
                else:
                    # it fits, so prep to try one longer
                    _last_fit = _check
        # done while, return results
        return results
