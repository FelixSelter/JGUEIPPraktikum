from typing import Any

from ecs_pattern import entity, EntityManager

from animation import AnimationComponent, Animation, AnimationFrame
from assets import Assets
from components import SpriteComponent, GravityComponent, TransformComponent, ScoreComponent, MovementComponent, \
    HitboxComponent, TileColliderComponent
from entities.coin_entity import CoinEntity
from util.math import Vec2


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent, ScoreComponent, AnimationComponent):
    def serialize(self):
        return PlayerData(self.position)


def playerCollisionHandler(player: PlayerEntity, item: Any, entities: EntityManager):
    if isinstance(item, CoinEntity):
        player.score += item.treasure
        entities.delete_buffer_add(item)


class PlayerData:
    def __init__(self, position: Vec2):
        self.position = position

    def deserialize(self):
        return PlayerEntity(
            position=Vec2(3, 8),
            width=1,
            height=1,
            sprite=Assets.get().playerImgs[0],
            acceleration=Vec2(0, 0),
            speed=Vec2(0, 0),
            hitboxEventHandler=playerCollisionHandler,
            tileCollisionEventHandler=lambda _a, _b, _c: None,
            score=0,
            animations={"default": Animation(
                [AnimationFrame(Assets.get().playerImgs[0], 0.3), AnimationFrame(Assets.get().playerImgs[1], 0.3),
                 AnimationFrame(Assets.get().playerImgs[2], 0.3)])},
            activeAnimation="default",
            currentTime=0,
            loopAnimation=True
        )
