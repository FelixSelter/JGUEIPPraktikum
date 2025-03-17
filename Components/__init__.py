from typing import Any, Callable

from ecs_pattern import component
from pygame import Surface

from util.math import Vec2


@component
class SpriteComponent:
    sprite: Surface


@component
class TransformComponent:
    position: Vec2
    width: float
    height: float


@component
class MovementComponent:
    acceleration: Vec2
    speed: Vec2


@component
class HitboxComponent:
    collisionCallback: Callable[[Any], None]
