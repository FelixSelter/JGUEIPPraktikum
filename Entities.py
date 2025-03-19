from Assets import Assets
from ecs_pattern import entity

from Animation import AnimationComponent
from Components import EnemyNameComponent, SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, \
    TileColliderComponent, \
    GravityComponent, TreasureComponent, ScoreComponent
from util.math import Vec2

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



