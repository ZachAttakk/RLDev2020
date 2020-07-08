"""Entity component basic class"""
from __future__ import annotations

from pygame.surface import Surface
from typing import Tuple, TypeVar, TYPE_CHECKING
import copy

if TYPE_CHECKING:
    from map_objects.game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """Basic entity object"""

    def __init__(self,
                 sprite: dict,
                 name: str = "<Unnamed>",
                 blocks_movement: bool = False,
                 ):
        """Create new entity with position and tile sprite"""

        self.pos = [0, 0]
        self.sprite = sprite

        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, gamemap: GameMap, pos: Tuple[int, int] = (0, 0)) -> T:
        """Spawn a copy of this instance at the gives location."""
        clone = copy.deepcopy(self)
        clone.pos = pos
        gamemap.entities.add(clone)
        return clone

    def move(self, delta=(0, 0)):
        """Move entity by an offset

        Args:
            delta (x, y) (tuple): movement in cells
        """
        # Move the entity by a given amount
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def place(self, position: Tuple[int, int] = (0, 0)):
        """Place entity without movement."""
        self.pos = list(position) or [0, 0]

    @property
    def position(self) -> Tuple[int, int]:
        """Return entity tile position in tuple

        Returns:
            tuple: (x,y)
        """
        return tuple(self.pos)
