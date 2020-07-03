"""Entity component basic class"""
from pygame.surface import Surface
from typing import Tuple


class Entity:
    """Basic entity object"""

    def __init__(self, sprite=None, pos=(0, 0)):
        """Create new entity with position and tile sprite

        Args:
            sprite (surface): sprite image
            pos (tuple, optional): Initial position of entity. Defaults to (0, 0).
        """

        self.pos = list(pos) or [0, 0]
        if sprite is not None:
            if isinstance(sprite, Surface):
                self.sprite = sprite
            else:
                # FIXME: What do we do if no sprite is passed?
                pass
        self.sprite = sprite

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
