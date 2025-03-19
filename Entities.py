from ecs_pattern import entity

from Components import SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, \
    TileColliderComponent, \
    GravityComponent, TreasureComponent, ScoreComponent


@entity
class Tile(SpriteComponent, TransformComponent):
    pass


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent, ScoreComponent):
    pass


@entity
class CoinEntity(SpriteComponent, TransformComponent, HitboxComponent, TreasureComponent):
    pass


@entity
class EnemyEntity(SpriteComponent, TransformComponent, HitboxComponent, TileColliderComponent, GravityComponent, MovementComponent):
    pass
