from ecs_pattern import entity

from assets import Assets
from components.clickable_component import ClickableComponent
from components.hitbox_component import HitboxComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from components.power_up_component import PowerUpComponent
from util.additional_math import Vec2
from animation import AnimationComponent, Animation, AnimationFrame


@entity
class PowerUpEntity(SpriteComponent, TransformComponent, HitboxComponent, PowerUpComponent, AnimationComponent,
                 ClickableComponent):

    def serialize(self):
        return PowerUpData(self.position, self.power)


class PowerUpData:
    def __init__(self, position: Vec2, power: int, sprite: str):
        self.position = position
        self.power = power
        self.sprite = sprite

    def deserialize(self):
        return PowerUpEntity(
            position=self.position,
            width=0.5,
            height=0.5,
            sprite=Assets.get().collectibleImgsDict[self.sprite][0],
            hitboxEventHandler=None,
            power=self.power,
            powerDelay=5,
            animations={"spinning": Animation(
                [AnimationFrame(Assets.get().collectibleImgsDict[self.sprite][i], 0.1) for i in
                 range(len(Assets.get().collectibleImgsDict[self.sprite]))])},
            activeAnimation="spinning",
            currentTime=0,
            loopAnimation=True,
            click_event_handler=None
        )
