import numpy as np  # type: ignore

tile_dt = np.dtype(
    [
        ("id", np.int),
        ("walkable", np.bool),
        ("transparent", np.bool)
    ]
)


def new_tile(*, id: str, walkable: int, transparent: int) -> np.ndarray:
    """Make a new tile

    Args:
        name (str): name for this type of tile
        walkable (bool): can be traversed
        transparent (bool): can be seen throug
    """
    return np.array((id, walkable, transparent), dtype=tile_dt)


floor = new_tile(id=1, walkable=True, transparent=True,)
wall = new_tile(id=2, walkable=False, transparent=False,)
