import spritesheet
import pygame.surface
from map_objects import tile_types


def render_entities(con, entities, tile_size=16):
    # Draw all entities in the list
    for _ent in entities:
        draw_entity(con, _ent, tile_size)


def draw_entity(con, entity, tile_size=16):
    # draw character
    # player = pygame.image.load(os.path.join("tiles", CONFIG.Sprites.player.value))
    # calculate position
    _x_pos = entity.pos[0] * tile_size
    _y_pos = entity.pos[1] * tile_size

    con.blit(entity.sprite, (_x_pos, _y_pos))


def render_map(con, game_map, sheets, sprites, tile_size=16):

    wall_sprite_data = sprites.get("wall")
    wall_sprite_image = sheets.get(wall_sprite_data.get(
        "sheet")).sprite_at(wall_sprite_data.get("values"))
    floor_sprite_data = sprites.get("floor")
    floor_sprite_image = sheets.get(floor_sprite_data.get(
        "sheet")).sprite_at(floor_sprite_data.get("values"))

    for y in range(game_map.height):
        for x in range(game_map.width):
            # get tile info for rendering
            tile = game_map.tiles[x][y]
            explored = game_map.explored[x][y]
            visible = game_map.visible[x][y]

            # if it's not explored, we don't show it at all
            if explored:
                if tile == tile_types.wall:
                    draw_tile(con, x, y, wall_sprite_image, tile_size)
                else:
                    draw_tile(con, x, y, floor_sprite_image, tile_size)

                # if it's not currently in LOS, we draw grey over it.
                if not visible:
                    darken = pygame.Surface(
                        (tile_size, tile_size)).convert_alpha()
                    darken.fill(sheets.get(
                        wall_sprite_data.get("sheet")).empty)
                    darken.fill(sheets.get(
                        wall_sprite_data.get("sheet")).darkened)
                    draw_tile(con, x, y, darken, tile_size)


def draw_tile(con, x, y, tile, tile_size):
    _x = x * tile_size
    _y = y * tile_size
    con.blit(tile, (_x, _y))
