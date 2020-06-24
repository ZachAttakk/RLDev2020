class Tile:
    """
    A tile on the map. It may or may not be blocked, and may on may not block LOS
    """

    def __init__(self, blocked, block_sight=None):
        """
        A tile on the map.

        Args:
            blocked (bool): True if tile blocks movement
            block_sight (bool, optional): True if tile blocks line of sight. Defaults to the same as blocked.
        """
        self.blocked = blocked
        self.block_sight = block_sight or blocked
