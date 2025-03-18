from ecs_pattern import entity

from Components import SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent, \
    GravityComponent


@entity
class Tile(SpriteComponent, TransformComponent):
    pass


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent):
    pass
