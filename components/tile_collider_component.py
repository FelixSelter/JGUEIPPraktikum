from enum import Enum
from typing import Callable, Any

from ecs_pattern import EntityManager, component

from util import CollisionDirection


@component
class TileColliderComponent:
    """
    Prevents movable entities from entering tiles
    Requires HitboxComponent, MovementComponent
    """
    # tileBottomLeftRightCollisionEventHandler(this,direction,tile,entities)
    # not executed if colliding with the top of tiles like walking on the ground
    tileBottomLeftRightCollisionEventHandler: Callable[[Any, CollisionDirection, (int, int),
                                                        EntityManager], None] | None

    # Only called if colliding with the top of tiles like walking on the ground
    # tileTopCollisionEventHandler(this,tile,entities)
    tileTopCollisionEventHandler: Callable[[Any, (int, int),
                                            EntityManager], None] | None
