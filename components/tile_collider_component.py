from enum import Enum
from typing import Callable, Any

from ecs_pattern import EntityManager, component


class TileCollisionDirection(Enum):
    Top = 0,
    Bottom = 1,
    Left = 2,
    Right = 3


@component
class TileColliderComponent:
    """
    Prevents movable entities from entering tiles
    Requires HitboxComponent, MovementComponent
    """
    tileCollisionEventHandler: Callable[[Any, TileCollisionDirection,
                                         EntityManager], None] | None  # tileCollisionEventHandler(this,direction,entities)
