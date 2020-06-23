class Entity:
    def __init__(self, pos=(0, 0), sheet="base", sprite=(0, 0)):
        """Create new entity with position and tile sprite

        Args:
            pos (x,y), optional: Position on grid. Defaults to (0, 0).
            sheet (str), optional: Name of spritesheet. Defaults to "base".
            sprite (column,row), optional: Positon of sprite on sheet. Defaults to (0, 0).
        """
        self.pos = list(pos)
        self.spritesheet = sheet
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
        return tuple(self.pos)
