from ecs_pattern import entity

from assets import Assets
from components.clickable_component import ClickableComponent
from components.hitbox_component import HitboxComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from components.treasure_component import TreasureComponent
from util.additional_math import Vec2
from animation import AnimationComponent, Animation, AnimationFrame


@entity
class CoinEntity(SpriteComponent, TransformComponent, HitboxComponent, TreasureComponent, AnimationComponent,
                 ClickableComponent):

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
            sprite=Assets.get().coinImgs[0],
            hitboxEventHandler=None,
            treasure=1,
            animations={"spinning": Animation(
                [AnimationFrame(Assets.get().coinImgs[0], 0.1), AnimationFrame(Assets.get().coinImgs[1], 0.1),
                 AnimationFrame(Assets.get().coinImgs[2], 0.1), AnimationFrame(Assets.get().coinImgs[3], 0.1)])},
            activeAnimation="spinning",
            currentTime=0,
            loopAnimation=True,
            click_event_handler=None
        )
