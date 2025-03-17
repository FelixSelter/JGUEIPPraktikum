from ecs_pattern import entity

from Components import SpriteComponent, TransformComponent, MovementComponent, HitboxComponent


@entity
class Tile(SpriteComponent, TransformComponent, HitboxComponent):
    pass


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent):
    pass
