"""Action object and its derivitives"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity


class Action:
    '''Generic action'''

    def __init__(self, entity: Actor):
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return engine for this action"""
        return self.entity.GAMEMAP.engine

    def perform(self) -> None:
        """
        REQUIRED OVERRIDE
        Perform this action with the entities needed to determine its scope.
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
    def target_actor(self) -> Optionall[Actor]:
        """Returns the actor at this action's destination"""
        return self.engine.GAMEMAP.get_actor_at(self.dest_xy)

    def perform(self):
        return super().perform()


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
        elif self.engine.GAMEMAP.get_blocking_entity_at((dest_x, dest_y)):
            validation = False  # destination is occupied by blocking entity

        if validation:
            self.entity.move((self.d_x, self.d_y))  # delta is tuple


class ActionMelee(ActionWithDirection):
    """Action that attacks the entity in a space, but doesn't move"""

    def perform(self):
        target = self.target_actor
        if not target:
            return  # No entity to attack

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            print(f"{attack_desc} for {damage} hit points.")
            target.fighter.hp -= damage
        else:
            print(f"{attack_desc} but does no damage.")


class ActionWait(Action):
    """Hurry up and do nothing"""

    def __init__(self, entity):
        """Space intentionally left blank"""
        pass

    def perform(self):
        """Space intentionally left blank"""
        pass
