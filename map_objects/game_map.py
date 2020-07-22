"""Make a map filled with walls

    Returns:
        GameMap: A map full of walls
    """
from __future__ import annotations

from typing import Iterable, Iterator, Optional, Tuple, TYPE_CHECKING
import numpy as np
from map_objects import tile_types
from entity import Actor

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height

        self.engine = engine
        self.entities = set(entities)

        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F")  # visible tiles
        self.explored = np.full(
            (width, height), fill_value=False, order="F")  # seen before tiles

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this map's living actors"""
        yield from (
            entity for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    def get_names_at_location(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y) or not self.visible[x, y]:
            return ""

        names = ", ".join(
            entity.name for entity in self.entities if entity.position == (x, y)
        )

        return names.capitalize()

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and f are inside the bounds of the map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at(self, pos: Tuple[int, int]) -> Optional[Entity]:
        """Get the entity in this space if it's blocking. There should only be one."""
        for entity in self.entities:
            if entity.blocks_movement and entity.position == pos:
                return entity
        return None

    def get_actor_at(self, pos: Tuple[int, int]) -> Optional[Actor]:
        for actor in self.actors:
            if actor.position == pos:
                return actor
        return None
