from ecs_pattern import component

from util.additional_math import Vec2


@component
class MovementComponent:
    """
    Requires TransformComponent
    """
    acceleration: Vec2
    speed: Vec2
