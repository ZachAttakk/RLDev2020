class Entity:
    def __init__(self, sprite=None, pos=(0, 0)):
        """Create new entity with position and tile sprite

        Args:
            sprite (surface): sprite image
            pos (tuple, optional): Initial position of entity. Defaults to (0, 0).
        """

        self.pos = list(pos) or [0, 0]
        self.sprite = sprite

    def move(self, delta=(0, 0)):
        """Move

        Args:
            delta (x, y) (tuple): movement in cells
        """
        # Move the entity by a given amount
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def get_position(self):
        """Return entity tile position in tuple

        Returns:
            tuple: (x,y)
        """
        return tuple(self.pos)
