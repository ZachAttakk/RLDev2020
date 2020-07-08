
import pygame
import spritesheet
import copy

from engine import Engine
from procgen import generate_dungeon
from config import Config as CONFIG
import entity_factories


def main() -> None:

    # It has to start somewhere, it has to start sometime.
    # What better place than here, what better time than now.
    pygame.init()

    # get surface size
    scale = CONFIG.Display.get("scale")

    # make main surface
    surface_main = pygame.display.set_mode(
        size=(int(CONFIG.Display.get("game_width") * scale), int(CONFIG.Display.get("game_height") * scale)))

    # preload sprite sheets
    spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)

    # make player and rando NPC
    # TODO: Magic numbers!
    player = copy.deepcopy(entity_factories.player)

    # generate map
    # max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    game_map = generate_dungeon(CONFIG.Game.get("rooms_max"),
                                CONFIG.Game.get("room_size_min"),
                                CONFIG.Game.get("room_size_max"),
                                CONFIG.Game.get("map_width"),
                                CONFIG.Game.get("map_height"),
                                CONFIG.Game.get("monsters_per_room"),
                                player)

    engine = Engine(game_map, player)

    # gobal quit flag
    should_quit = False

    # MAIN LOOP
    while not should_quit:

        # handle inputs

        events = pygame.event.get(pump=True)
        if len(events) > 0:
            try:
                engine.handle_events(events)
            except (SystemExit):
                should_quit = True
                continue

        # print to screen
        engine.render(surface_main)

    # ... and we're done!
    pygame.quit()


if __name__ == "__main__":
    main()
