from ecs_pattern import component

from util.additional_math import Vec2


@component
class TransformComponent:
    position: Vec2
    width: float
    height: float
