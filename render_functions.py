import spritesheet


def render_entities(con, entities, tile_size=16):
    # Draw all entities in the list
    for _ent in entities:
        draw_entity(con, _ent, tile_size)

    #libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


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
            wall = game_map.tiles[x][y].block_sight

            if wall:
                draw_tile(con, x, y, wall_sprite_image, tile_size)
            else:
                draw_tile(con, x, y, floor_sprite_image, tile_size)


def draw_tile(con, x, y, tile, tile_size):
    _x = x * tile_size
    _y = y * tile_size
    con.blit(tile, (_x, _y))
