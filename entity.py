"""Entity component basic class"""
from __future__ import annotations

from pygame.surface import Surface
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING
import copy
from render_order import RenderOrder


if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.fighter import Fighter
    from map_objects.game_map import GameMap

T = TypeVar("T", bound="Entity")


class Entity:
    """Basic entity object"""

    parent: GameMap

    def __init__(self, *,
                 parent: Optional[GameMap] = None,
                 sprite: Optional[dict] = None,
                 name: str = "<Unnamed>",
                 blocks_movement: bool = False,
                 render_order: RenderOrder = RenderOrder.CORPSE,
                 ):
        """Create new entity with position and tile sprite"""

        self.pos = [0, 0]
        self.sprite = sprite

        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

        if parent:
            # If gamemap isn't provided now, then it will be set later
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, pos: Tuple[int, int] = (0, 0)) -> T:
        """Spawn a copy of this instance at the gives location."""
        clone = copy.deepcopy(self)
        clone.pos = list(pos)
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def move(self, delta=(0, 0)):
        """Move entity by an offset

        Args:
            delta (x, y) (tuple): movement in cells
        """
        # Move the entity by a given amount
        self.pos[0] += delta[0]
        self.pos[1] += delta[1]

    def place(self, position: Tuple[int, int] = (0, 0), gamemap: Optional[GameMap] = None) -> None:
        """Place entity without movement."""
        self.pos = list(position) or [0, 0]
        if gamemap:
            if hasattr(self, "parent"):
                self.parent.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    @property
    def position(self) -> Tuple[int, int]:
        """Return entity tile position in tuple

        Returns:
            tuple: (x,y)
        """
        return tuple(self.pos)


class Actor(Entity):
    def __init__(self, *,
                 gamemap=None,
                 sprite=None,
                 name='<Unnamed>',
                 ai_cls: Type[BaseAI],
                 fighter: Fighter):

        super().__init__(parent=gamemap, sprite=sprite,
                         name=name, blocks_movement=True,
                         render_order=RenderOrder.ACTOR)

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can porform actions."""
        return bool(self.ai)
