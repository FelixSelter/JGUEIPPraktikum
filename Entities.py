from ecs_pattern import entity

from Animation import AnimationComponent
from Components import SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, \
    TileColliderComponent, \
    GravityComponent, TreasureComponent, ScoreComponent


@entity
class TileEntity(SpriteComponent, TransformComponent):
    pass


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent, ScoreComponent, AnimationComponent):
    pass


@entity
class CoinEntity(SpriteComponent, TransformComponent, HitboxComponent, TreasureComponent):
    pass
