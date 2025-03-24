from ecs_pattern import entity

from assets import Assets
from components.hitbox_component import HitboxComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from components.treasure_component import TreasureComponent
from util.additional_math import Vec2
from animation import AnimationComponent, Animation, AnimationFrame


@entity
class CoinEntity(SpriteComponent, TransformComponent, HitboxComponent, TreasureComponent, AnimationComponent):

    def serialize(self):
        return CoinData(self.position, self.treasure)


class CoinData:
    def __init__(self, position: Vec2, treasure: int, sprite: str):
        self.position = position
        self.treasure = treasure
        self.sprite = sprite

    def deserialize(self):
        return CoinEntity(
            position=self.position,
            width=0.5,
            height=0.5,
            sprite=Assets.get().collectibleImgsDict[self.sprite][0],
            hitboxEventHandler=None,
            treasure=self.treasure,
            animations={"spinning": Animation(
                [AnimationFrame(Assets.get().collectibleImgsDict[self.sprite][i], 0.1) for i in
                 range(len(Assets.get().collectibleImgsDict[self.sprite]))])},
            activeAnimation="spinning",
            currentTime=0,
            loopAnimation=True
        )
