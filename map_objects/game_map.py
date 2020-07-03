"""Make a map filled with walls

    Returns:
        GameMap: A map full of walls
    """
import numpy as np
from map_objects import tile_types


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = np.full(
            (width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full(
            (width, height), fill_value=False, order="F")  # visible tiles
        self.explored = np.full(
            (width, height), fill_value=False, order="F")  # seen before tiles

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and f are inside the bounds of the map."""
        return 0 <= x < self.width and 0 <= y < self.height
