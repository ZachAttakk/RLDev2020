from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Tuple
import numpy as np

import pygame
import spritesheet
from config import Config as CONFIG
from map_objects import tile_types
from spritesheet import Spritesheet

if TYPE_CHECKING:
    from engine import Engine
    from map_objects.game_map import GameMap


def draw_entity(con, entity, image, tile_size=16):
    # calculate position
    _x_pos = entity.pos[0] * tile_size
    _y_pos = entity.pos[1] * tile_size

    con.blit(image, (_x_pos, _y_pos))


def render_map(con, game_map, sheets, sprites, tile_size=16):

    wall_sprite_data = sprites.get("wall")
    wall_sprite_image = sheets.get(wall_sprite_data.get(
        "sheet")).sprite_at(wall_sprite_data)

    floor_sprite_data = sprites.get("floor")
    floor_sprite_image = sheets.get(floor_sprite_data.get(
        "sheet")).sprite_at(floor_sprite_data)

    for y in range(game_map.height):
        for x in range(game_map.width):
            # get tile info for rendering
            tile = game_map.tiles[x][y]
            explored = game_map.explored[x][y]
            visible = game_map.visible[x][y]

            # if it's not explored, we don't show it at all
            if explored:
                if tile == tile_types.wall:
                    draw_tile(con, x, y, wall_sprite_image,
                              tile_size)
                else:
                    draw_tile(con, x, y, floor_sprite_image, tile_size)
                    pass

                # if it's not currently in LOS, we draw grey over it.
                if not visible:
                    darken = pygame.Surface(
                        (tile_size, tile_size)).convert()
                    darken.fill(CONFIG.get_colour("black"))
                    darkness = CONFIG.Display.get("darkness_opacity") or 0
                    darken.set_alpha(darkness)
                    draw_tile(con, x, y, darken, tile_size)

    # Render entities on visible tiles
    entities_sorted_for_rendering = sorted(
        game_map.entities, key=lambda x: x.render_order.value
    )
    for _ent in entities_sorted_for_rendering:
        # only render if visible
        _ent_pos = list(_ent.position)
        if game_map.visible[_ent_pos[0], _ent_pos[1]]:
            # get sprite
            ent_sprite_image = sheets.get(
                _ent.sprite.get("sheet")).sprite_at(_ent.sprite)
            draw_entity(con, _ent, ent_sprite_image, tile_size)


def render_names(con, game_map, position, font, tile_size=16):
    """Renders entity names at a position on the map, at that position on the map"""

    # first transpose the given pixel position to map position
    # TODO: When we implement offsets on the map, we'll have to take those into account
    tile_x, tile_y = position
    tile_x = int(tile_x/tile_size)
    tile_y = int(tile_y/tile_size)

    # get the entities at that position
    names = game_map.get_names_at_location(tile_x, tile_y)
    if names:
        # offset name so it's not behind the mouse
        x_pos = position[0] + font.get_linesize()
        y_pos = position[1] - font.get_linesize()
        render_outlined_text(
            con, names, (x_pos, y_pos), CONFIG.get_colour("white"), font, break_on_comma=True)


def render_text(con, text: str, position: Tuple[int, int], fg_col, fonts, break_on_comma=False):

    if isinstance(fonts, dict):
        font = fonts.get("mini")
    else:
        font = fonts

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
            render_text(
                text_surface, line, (0, y_offset), fg_col, font)
            y_offset += font.get_linesize()
    else:
        text_surface = font.render(
            text, False, CONFIG.get_colour(fg_col))

    con.blit(text_surface, position)


def render_outlined_text(con, text, position: Tuple[int, int], fg_col, fonts, break_on_comma=False):
    # 9 positions, either way of the middle

    for x in range(-1, 2):
        for y in range(-1, 2):
            temp_x, temp_y = position
            temp_x += x
            temp_y += y
            render_text(con, text, (temp_x, temp_y),
                        "black", fonts, break_on_comma)

    # and the actual text...
    render_text(con, text, position, fg_col, fonts, break_on_comma)


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


def draw_tile(con, x, y, tile, tile_size):
    _x = x * tile_size
    _y = y * tile_size
    con.blit(tile, (_x, _y))


def render_bar(con, current_value, max_value, total_width, font) -> None:
    bar_width = int(float(current_value) / max_value * total_width)

    _bar = pygame.Surface((total_width, 10)).convert()
    _bar.fill(CONFIG.get_colour("bar_empty"))
    if bar_width > 0:
        pygame.draw.rect(_bar, CONFIG.get_colour(
            "bar_filled"), pygame.Rect(0, 0, bar_width, 10))
    render_text(_bar, f"HP: {current_value}/{max_value}", (1, 0), CONFIG.get_colour(
        "white"), font)

    con.blit(_bar, (0, 0))


def make_window(size, sheets: Spritesheet, decorations, tile_size=16):
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
    _sheet = sheets.get(decorations.get("sheet"))
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
