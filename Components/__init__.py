from enum import Enum
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
    """
    Requires TransformComponent
    """
    acceleration: Vec2
    speed: Vec2


@component
class HitboxComponent:
    """
    Intersection between game objects excluding tiles
    Requires TransformComponent
    """
    hitboxEventHandler: Callable[[Any, Any], None]


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
    tileCollisionEventHandler: Callable[[TileCollisionDirection], None]


@component
class GravityComponent:
    """
    Requires MovementComponent
    """
    pass
