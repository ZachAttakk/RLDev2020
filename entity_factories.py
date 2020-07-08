from entity import Entity
from config import Config as CONFIG

player = Entity(sprite=CONFIG.Sprites.get("player"),
                name="Player", blocks_movement=True)
blue = Entity(sprite=CONFIG.Sprites.get("blue"),
              name="Blue", blocks_movement=True)
yellow = Entity(sprite=CONFIG.Sprites.get("yellow"),
                name="Yellow", blocks_movement=True)
