from typing import Callable, Any

from ecs_pattern import component, EntityManager


@component
class HitboxComponent:
    """
    Intersection between game objects excluding tiles
    Requires TransformComponent
    """
    hitboxEventHandler: Callable[[Any, Any, EntityManager], None] | None  # hitboxEventHandler(this, other, entities)
