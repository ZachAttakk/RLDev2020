from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from event_handlers import GameOverEventHandler
from config import Config as CONFIG
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor


class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hp: int, defense: int, power: int):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.parent.ai:
            self.die()

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovored = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovored

    def take_damage(self, amount: int) -> None:
        self.hp -= amount

    def die(self) -> None:
        if self.engine.PLAYER is self.parent:
            death_message = "You died!"
            death_message_colour = CONFIG.get_colour("player_die")
            self.engine.eventhandler = GameOverEventHandler(self.engine)
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_colour = CONFIG.get_colour("enemy_die")

        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.render_order = RenderOrder.CORPSE
        death_sprite = CONFIG.Sprites.get(self.parent.name.lower()+"_dead")
        if death_sprite:
            self.parent.sprite = CONFIG.Sprites.get(self.parent.name.lower()+"_dead")
        else:
            self.parent.sprite["fgcolour"] = CONFIG.get_colour("black")

        # from this point onwards, the entity name and the sprite doesn't match
        self.parent.name = f"remains of {self.parent.name}"

        self.engine.message_log.add_message(death_message, death_message_colour)
