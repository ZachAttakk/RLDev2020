from components.consumable import Consumable, HealingConsumable
from components.ai import BaseAI, Hostile
from components.fighter import Fighter
from entity import Actor, Item
from config import Config as CONFIG


player = Actor(name="Player", ai_cls=BaseAI, fighter=Fighter(hp=30, defense=2, power=5),)
# TODO Magic numbers!

blue = Actor(name="Blue",
             ai_cls=Hostile, fighter=Fighter(hp=10, defense=0, power=3),
             )
yellow = Actor(name="Yellow",
               ai_cls=Hostile, fighter=Fighter(hp=16, defense=1, power=4),
               )
health_potion = Item(name="Health Potion", consumable=HealingConsumable(amount=4),)
