from components.ai import BaseAI, Hostile
from components.fighter import Fighter
from entity import Actor
from config import Config as CONFIG


player = Actor(sprite=CONFIG.Sprites.get("player"),
               name="Player", ai_cls=BaseAI, fighter=Fighter(hp=30, defense=2, power=5),)
# TODO Magic numbers!

blue = Actor(sprite=CONFIG.Sprites.get("blue"), name="Blue",
             ai_cls=Hostile, fighter=Fighter(hp=10, defense=0, power=3),
             )
yellow = Actor(sprite=CONFIG.Sprites.get("yellow"), name="Yellow",
               ai_cls=Hostile, fighter=Fighter(hp=16, defense=1, power=4),
               )
