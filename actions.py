"""Action object and its derivitives"""
from __future__ import annotations
from enum import IntEnum

from typing import Optional, TYPE_CHECKING
from config import Config as CONFIG
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    '''Generic action'''

    def __init__(self, entity: Actor):
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return engine for this action"""
        return self.entity.parent.engine

    def perform(self) -> bool:
        """
        REQUIRED OVERRIDE
        Perform this action with the entities needed to determine its scope.
        Returns True if action takes a turn
        """
        raise NotImplementedError()


class ActionEscape(Action):
    '''Action that escapes whatever it's in'''

    def __init__(self):
        """Space intentionally left blank"""
        pass

    # TODO: Make it escape whatever it's in
    def perform(self) -> None:
        raise SystemExit()


class ActionFullscreen(Action):
    '''Action that changes from fullscreen to window and vice versa'''

    def __init__(self):
        """Space intentionally left blank"""
        pass

    def perform(self) -> None:
        pass


class ActionQuit(Action):
    '''Action that quits the game'''

    def __init__(self):
        """Space intentionally left blank"""
        pass

    def perform(self) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, d_x: int, d_y: int):
        super().__init__(entity)

        self.d_x = d_x
        self.d_y = d_y

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Return this action's destination"""
        dest_x, dest_y = self.entity.position
        dest_x += self.d_x
        dest_y += self.d_y
        return dest_x, dest_y

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the entity that's blocking this action, if any"""
        return self.engine.GAMEMAP.get_blocking_entity_at(self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Returns the actor at this action's destination"""
        return self.engine.GAMEMAP.get_actor_at(self.dest_xy)

    def perform(self):
        return super().perform()


class ActionWithPosition(Action):
    """Action that has a position"""

    def __init__(self, position: Tuple[int:int]):
        self.x = position[0]
        self.y = position[1]

    @property
    def position(self):
        return self.x, self.y


class ActionMouseMove(ActionWithPosition):
    def __init__(self, engine: Engine, position: Tuple[int, int]):
        super().__init__(position)
        self.engineref = engine

    def perform(self):
        self.engineref.mouse_position = self.position


class ActionBump(ActionWithDirection):
    """Action that checks whether to attack or move"""

    def perform(self):
        if self.target_actor:
            return ActionMelee(self.entity, self.d_x, self.d_y).perform()
        else:
            return ActionMove(self.entity, self.d_x, self.d_y).perform()


class ActionMove(ActionWithDirection):
    '''Action that moves the player'''

    def perform(self) -> None:

        # find destination tile
        dest_x, dest_y = self.dest_xy

        # safe unless invalidated
        validation = True

        # check if that tile is within the map
        if not self.engine.GAMEMAP.in_bounds(dest_x, dest_y):
            validation = False  # destination is out of bounds
        # check if the tile is walkable
        elif not self.engine.GAMEMAP.tiles["walkable"][dest_x, dest_y]:
            validation = False  # destination is blocked by a tile
        # check if there's an entity in the way
        elif self.engine.GAMEMAP.get_blocking_entity_at((dest_x, dest_y)):
            validation = False  # destination is occupied by blocking entity

        if validation:
            self.entity.move((self.d_x, self.d_y))  # delta is tuple
        else:
            raise exceptions.Impossible("That way is blocked.")
        # return true to trigger player turn
        return True


class ActionMelee(ActionWithDirection):
    """Action that attacks the entity in a space, but doesn't move"""

    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")  # No entity to attack

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"

        if self.entity is self.engine.PLAYER:
            attack_color = CONFIG.get_colour("player_atk")
        else:
            attack_color = CONFIG.get_colour("enemy_atk")

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} HP.", attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)

        # return true to trigger player turn
        return True


class ActionWait(Action):
    """Hurry up and do nothing"""

    def __init__(self, entity):
        """Space intentionally left blank"""
        pass

    def perform(self):
        """Return True to trigger player turn"""
        # return true to trigger player turn
        return True


class ActionItem(Action):
    def __init__(self, entity: Actor, item: Item, target_pos: Optional(Tuple[int, int]) = None):
        super().__init__(entity)
        self.item = item
        if not target_pos:
            target_pos = entity.position
        self.target_pos = target_pos

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this action's destination"""
        return self.engine.game_map.get_actor_at(self.target_pos)

    def perform(self) -> None:
        """Invoke the item's ability, this action will be given to provide context."""
        self.item.consumable.activate(self)
