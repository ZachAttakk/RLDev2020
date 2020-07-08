"""Procedural generation code"""
from __future__ import annotations  # because apparently typing isn't properly implemented in 3.8
from typing import Tuple, Iterator, List, TYPE_CHECKING
import random
import tcod
from entity import Entity
from map_objects.game_map import GameMap
from map_objects import tile_types
import entity_factories

if TYPE_CHECKING:
    from engine import Engine


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        """Generate rectangular room

        Args:
            x (int): x position
            y (int): y position
            width (int): width
            height (int): height
        """
        self.x_1 = x
        self.y_1 = y
        self.x_2 = x + width
        self.y_2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        """Returns 

        Returns:
            Tuple[int, int]: [description]
        """
        center_x = int((self.x_1+self.x_2)/2)
        center_y = int((self.y_1 + self.y_2) / 2)
        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Returns the area of the room excluding the bounding wall"""
        return slice(self.x_1 + 1, self.x_2), slice(self.y_1 + 1, self.y_2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom"""
        return (self.x_1 <= other.x_2
                and self.x_2 >= other.x_1
                and self.y_1 <= other.y_2
                and self.y_2 >= other. y_1)

    # end of RectangularRoom class


def generate_dungeon(max_rooms: int,
                     room_min_size: int,
                     room_max_size: int,
                     map_width: int,
                     map_height: int,
                     monsters_per_room: int,
                     engine: Engine) -> GameMap:
    """Generates a dungeon map"""

    # get the player
    player = engine.PLAYER
    # make blank dungeon
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    # list that will contain our rooms
    rooms: List[RectangularRoom] = []

    # for as many rooms as we can, but if one of them overlaps we just keep going, meaning there will be one less
    for r in range(max_rooms):
        # make room of random size
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        # find place to put room
        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # create rectangular room from this
        new_room = RectangularRoom(x, y, room_width, room_height)

        # check if it overlaps another room
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue
            # This room overlaps another.
            # Rather than try to move it, just make a now one

        # now we can safely "dig out" the room
        dungeon.tiles[new_room.inner] = tile_types.floor

        # connect all the rooms, one by one in a line

        if len(rooms) == 0:  # first room, place player here
            player.place(new_room.center, dungeon)
        else:  # all rooms after the first
            # Dig out a tunnel between this and the previous room
            # index -1 gets the last item in a list
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # add baddies
        place_entities(new_room, dungeon, monsters_per_room)

        # finally, add the new room to the list so we can test future rooms against it
        rooms.append(new_room)

    # We've reached the max number of rooms
    return dungeon


def place_entities(room: RectangularRoom, dungeon: GameMap, max_monsters_per_room: int) -> None:
    # how many monsters?
    number_of_monsters = random.randint(0, max_monsters_per_room)

    # place that many
    for i in range(number_of_monsters):
        x = random.randint(room.x_1 + 1, room.x_2 - 1)
        y = random.randint(room.y_1 + 1, room.y_2 - 1)

        prospective_pos = (x, y)
        if not any(entity.position == prospective_pos for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.blue.spawn(dungeon, (x, y))
            else:
                entity_factories.yellow.spawn(dungeon, (x, y))


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    x_1, y_1 = start
    x_2, y_2 = end
    if random.random() < 0.5:
        # horizontal first
        corner_x, corner_y = x_2, y_1
    else:
        # vertical first
        corner_x, corner_y = x_1, y_2

    # generate coordinates for the tunnel
    for x, y in tcod.los.bresenham((x_1, y_1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x_2, y_2)).tolist():
        yield x, y
