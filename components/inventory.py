from __future__ import annotations


from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int = 0) -> None:
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Removes an item from the inventory and puts it back on the map
        """

        self.items.remove(item)
        item.place(self.parent.position, self.gamemap)

        self.engine.message_log.add_message(f"You dropped the {item.name}.")
