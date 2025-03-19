from ecs_pattern import entity

from Assets import Assets
from Components import SpriteComponent, TransformComponent, MovementComponent, \
    HitboxComponent, \
    TreasureComponent
from util.math import Vec2


@entity
class CoinEntity(SpriteComponent, TransformComponent, HitboxComponent, TreasureComponent):

    def serialize(self):
        return CoinData(self.position, self.treasure)


class CoinData:
    def __init__(self, position: Vec2, treasure: int):
        self.position = position
        self.treasure = treasure

    def deserialize(self):
        return CoinEntity(
            position=self.position,
            width=0.5,
            height=0.5,
            sprite=Assets.get().coinImg,
            hitboxEventHandler=lambda _a, _b, _c: None,
            treasure=1
        )
