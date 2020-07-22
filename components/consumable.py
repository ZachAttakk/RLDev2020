from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
from components.base_component import BaseComponent
from config import Config as CONFIG
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_ection(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item """
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """ Invoke this items ability.

        'action' is the context for this activation
        """
        raise NotImplementedError()


class HealingConsumable(Consumable):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recavered} HP!",
                CONFIG.get_colour("health_recovered"),)
        else:
            raise Impossible("Your health is already full.")
