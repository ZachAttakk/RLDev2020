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
        self.parent.name = f"remains of {self.parent.name}"

        # TODO: I don't like modifying sprite colours directly
        self.parent.sprite["fgcolour"] = CONFIG.get_colour("black")

        self.engine.message_log.add_message(death_message, death_message_colour)
