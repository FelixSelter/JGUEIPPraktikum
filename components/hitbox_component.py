from typing import Callable, Any

from ecs_pattern import component, EntityManager

from util import CollisionDirection


@component
class HitboxComponent:
    """
    Intersection between game objects excluding tiles
    Requires TransformComponent
    """
    hitboxEventHandler: Callable[[Any, Any, CollisionDirection,
                                  EntityManager], None] | None  # hitboxEventHandler(this, other, direction, entities)
