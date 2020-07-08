"""Action object and its derivitives"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    '''Generic action'''

    def perform(self, engine: Engine, entity: Entity) -> None:
        """
        REQUIRED OVERRIDE
        Perform this action with the entities needed to determine its scope.

        Args:
            engine (Engine): scope in which the action is to be performed
            entity (Entity): object perfortming the action

        """
        raise NotImplementedError()


class ActionEscape(Action):
    '''Action that escapes whatever it's in'''

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionQuit(Action):
    '''Action that quits the game'''

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, d_x: int, d_y: int):
        super().__init__()

        self.d_x = d_x
        self.d_y = d_y

    def perform(self, engine: Engine, entity: Entity):
        return super().perform(engine, entity)


class ActionBump(ActionWithDirection):
    """Action that checks whether to attack or move"""

    def perform(self, engine: Engine, entity: Entity):
        # find destination tile
        dest_x, dest_y = entity.position
        dest_x += self.d_x
        dest_y += self.d_y

        if engine.GAMEMAP.get_blocking_entity_at((dest_x, dest_y)):
            return ActionMelee(self.d_x, self.d_y).perform(engine, entity)

        else:
            return ActionMove(self.d_x, self.d_y).perform(engine, entity)


class ActionMove(ActionWithDirection):
    '''Action that moves the player'''

    def perform(self, engine: Engine, entity: Entity) -> None:

        # find destination tile
        dest_x, dest_y = entity.position
        dest_x += self.d_x
        dest_y += self.d_y

        # safe unless invalidated
        validation = True

        # check if that tile is within the map
        if not engine.GAMEMAP.in_bounds(dest_x, dest_y):
            validation = False  # destination is out of bounds
        # check if the tile is walkable
        elif not engine.GAMEMAP.tiles["walkable"][dest_x, dest_y]:
            validation = False  # destination is blocked by a tile
        elif engine.GAMEMAP.get_blocking_entity_at((dest_x, dest_y)):
            validation = False  # destination is occupied by blocking entity

        if validation:
            entity.move((self.d_x, self.d_y))  # delta is tuple


class ActionMelee(ActionWithDirection):
    """Action that attacks the entity in a space, but doesn't move"""

    def perform(self, engine: Engine, entity: Entity):
        # find destination tile
        dest_x, dest_y = entity.position
        dest_x += self.d_x
        dest_y += self.d_y
        target = engine.GAMEMAP.get_blocking_entity_at((dest_x, dest_y))
        if not target:
            return  # No entity to attack

        print(f"You kick the {target.name}, much to its annoyance!")
