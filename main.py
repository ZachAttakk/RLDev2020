
import pygame
import spritesheet

from config import Config
from engine import Engine
from entity import Entity
from procgen import generate_dungeon


def main() -> None:

    # It has to start somewhere, it has to start sometime.
    # What better place than here, what better time than now.
    pygame.init()

    # Grab config
    CONFIG = Config()

    # get surface size
    scale = CONFIG.Game.get("scale")

    # make main surface
    surface_main = pygame.display.set_mode(
        size=(int(CONFIG.Game["game_width"] * scale), int(CONFIG.Game["game_height"] * scale)))

    # preload sprite sheets
    spritesheets = spritesheet.get_sheets(CONFIG.SpriteSheets)

    # make player and rando NPC
    # TODO: Magic numbers!
    player = Entity(spritesheets.get(CONFIG.Sprites.get("player").get(
        "sheet")).sprite_at(CONFIG.Sprites.get("player").get("values")), (7, 5))
    npc = Entity(spritesheets.get(CONFIG.Sprites.get("npc").get(
        "sheet")).sprite_at(CONFIG.Sprites.get("npc").get("values")), (3, 3))

    entities = [player, npc]

    # generate map
    # max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    game_map = generate_dungeon(CONFIG.Game.get("rooms_max"),
                                CONFIG.Game.get("room_size_min"),
                                CONFIG.Game.get("room_size_max"),
                                CONFIG.Game.get("map_width"),
                                CONFIG.Game.get("map_height"),
                                player)

    engine = Engine(entities, game_map, player, CONFIG)

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
