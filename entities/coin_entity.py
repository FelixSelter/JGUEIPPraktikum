from ecs_pattern import entity

from assets import Assets
from components.hitbox_component import HitboxComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from components.treasure_component import TreasureComponent
from util.additional_math import Vec2


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
            hitboxEventHandler=None,
            treasure=1
        )
