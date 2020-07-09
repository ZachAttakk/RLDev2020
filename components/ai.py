from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING
import numpy as np  # type: ignore
import tcod

from actions import Action, ActionMelee, ActionMove, ActionWait
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self):
        raise NotImplementedError()


class Hostile(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        # get player as target
        target = self.engine.PLAYER

        # how far is the player?
        d_x, d_y = tuple(np.subtract(target.position, self.entity.position))
        distance = max(abs(d_x), abs(d_y))  # chebyshev distance

        # if I'm visible, move or attack
        if self.engine.GAMEMAP.visible[self.entity.position]:
            if distance <= 1:  # within attack range
                return ActionMelee(self.entity, d_x, d_y).perform()

            # update path after hit
            self.path = self.get_path_to(target.position)

            # if I have a path, follow it
            if self.path:
                dest = self.path.pop(0)
                # make movement a delta
                return ActionMove(
                    self.entity, *np.subtract(dest, self.entity.position)
                ).perform()

        # if I haven't returned by now, just wait
        return ActionWait(self.entity).perform()

    def get_path_to(self, dest: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Compute and return the path to a target position.
        If there's no valid path, then return an empty string"""

        # Copy the walkable array (all costs are 1)
        cost = np.array(self.entity.GAMEMAP.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.GAMEMAP.entities:
            if entity.blocks_movement and cost[entity.position]:
                # if the entity blocks movement...
                # and its position exists in the walkable tiles
                # make that tile difficult to walk to
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.position] += 10

        # Create graph from the cost array and pass that graph to the pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root(self.entity.position)  # start position

        # Compute the path to the destination
        # Remember to remove the starting point,
        # otherwise the first action is moving to the current spot
        path: List[List[int]] = pathfinder.path_to(dest)[1:].tolist()
        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [tuple(index) for index in path]
