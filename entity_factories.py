from entity import Entity
from config import Config as CONFIG

player = Entity(CONFIG.Sprites.get("player"), "Player", True)
blue = Entity(CONFIG.Sprites.get("blue"), "Blue", True)
yellow = Entity(CONFIG.Sprites.get("yellow"), "Yellow", True)
