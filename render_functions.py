import spritesheet


def render_entities(con, entities, tile_size=16, tile_gap=0):
    # Draw all entities in the list
    for _ent in entities:
        draw_entity(con, _ent, tile_size, tile_gap)

    #libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def draw_entity(con, entity, tile_size=16, tile_gap=0):
    # draw character
    # player = pygame.image.load(os.path.join("tiles", CONFIG.Sprites.player.value))
    ss = spritesheet.spritesheet(
        entity.spritesheet, tile_size, tile_gap)
    image = ss.sprite_at(entity.sprite)
    # calculate position
    _x_pos = entity.pos[0] * ss.tile_size
    _y_pos = entity.pos[1] * ss.tile_size

    con.blit(image, (_x_pos, _y_pos))
