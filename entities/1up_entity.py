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
class LiveUpEntity(SpriteComponent, TransformComponent, HitboxComponent, ClickableComponent):

    def serialize(self):
        return LiveUpData(self.position)


class LiveUpData:
    def __init__(self, position: Vec2):
        self.position = position

    def deserialize(self):
        return LiveUpEntity(
            position=self.position,
            width=0.5,
            height=0.5,
            sprite=Assets.get().melonImg,
            hitboxEventHandler=None,
            click_event_handler=None
        )
