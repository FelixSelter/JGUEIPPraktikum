from ecs_pattern import component
from pygame import Surface


@component
class SpriteComponent:
    sprite: Surface
