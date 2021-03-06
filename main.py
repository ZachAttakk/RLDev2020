
from numpy.core.fromnumeric import trace
import pygame
import copy
import traceback
import sys

from engine import Engine
from procgen import generate_dungeon
from config import Config as CONFIG
import entity_factories


def main() -> None:

    # It has to start somewhere, it has to start sometime.
    # What better place than here, what better time than now.
    pygame.display.init()
    pygame.font.init()

    # make main surface
    surface_main = pygame.display.set_mode(
        size=(int(CONFIG.Display.get("game_width")),
              int(CONFIG.Display.get("game_height"))),
        flags=pygame.SCALED | pygame.RESIZABLE)

    # make player and rando NPC
    # TODO: Magic numbers!
    player = copy.deepcopy(entity_factories.player)

    # start the engine
    engine = Engine(player)

    # test message log.
    engine.message_log.add_message("Welcome to the game!")
    engine.message_log.add_message("These are test messages to see how the text wrapping will work.")

    # generate map
    # max_rooms, room_min_size, room_max_size, map_width, map_height, player)
    engine.GAMEMAP = generate_dungeon(CONFIG.Game.get("rooms_max"),
                                      CONFIG.Game.get("room_size_min"),
                                      CONFIG.Game.get("room_size_max"),
                                      CONFIG.Game.get("map_width"),
                                      CONFIG.Game.get("map_height"),
                                      CONFIG.Game.get("monsters_per_room"),
                                      CONFIG.Game.get("potions_per_room"),
                                      engine=engine)

    # Do the first FOV update for where the player stands
    engine.update_fov()

    # gobal quit flag
    should_quit = False

    # MAIN LOOP
    while not should_quit:

        # handle events
        try:
            engine.eventhandler.handle_events()
        except (SystemExit):
            should_quit = True
            continue
        except Exception:
            traceback.print_exc()  # print error to stderr.
            # then print error to message log.
            engine.message_log.add_message(traceback.format_exc(), CONFIG.get_colour("error"))

        # print to screen
        engine.render(surface_main)

    # ... and we're done!
    pygame.quit()


if __name__ == "__main__":
    main()
