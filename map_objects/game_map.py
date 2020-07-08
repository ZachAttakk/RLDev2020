"""Make a map filled with walls

    Returns:
        GameMap: A map full of walls
    """
from __future__ import annotations

from typing import Iterable, Optional, Tuple, TYPE_CHECKING
import numpy as np
from map_objects import tile_types

if TYPE_CHECKING:
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

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and f are inside the bounds of the map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_blocking_entity_at(self, pos: Tuple[int, int]) -> Optional[Entity]:
        """Get the entity in this space if it's blocking. There should only be one."""
        for entity in self.entities:
            if entity.blocks_movement and entity.position == pos:
                return entity
        return None
