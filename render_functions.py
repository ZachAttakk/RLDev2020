from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Tuple
import spritesheet
import pygame
from config import Config as CONFIG
from map_objects import tile_types


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


def render_text(con, text, position: Tuple[int, int], fg_col, fonts):

    if isinstance(fonts, dict):
        font = fonts.get("mini")
    else:
        font = fonts
        text_surface = font.render(
            text, False, CONFIG.get_colour(fg_col))
    con.blit(text_surface, position)


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
    render_text(_bar, f"HP: {current_value}/{max_value}", (1, 0), font)

    con.blit(_bar, (0, 0))
