import tcod as libtcod
from input_handlers import handle_keys


def main():
    '''Main engine function'''
    # TODO: Magic numbers: screen size
    screen_width = 80
    screen_height = 50

    # set player default position
    # TODO: Magin number: player position
    player_x = int(screen_width // 2)
    player_y = int(screen_height // 2)

    # set font to default png
    # TODO: Magic numbers: Window name
    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, 'RLDev2020')

    # make default console
    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # main loop
    while not libtcod.console_is_window_closed():

        # print to screen
        libtcod.console_clear(con)
        libtcod.console_set_default_foreground(con, libtcod.white)

        # this draws the @
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()

        # FIXME: Why is this line here?
        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

        # get inputs
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        action = handle_keys(key)

        move = action.get('move')
        should_exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if should_exit:
            return True
            # FIXME this feels super janky. Why are we simply returning true from the main loop?

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
