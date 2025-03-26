from ecs_pattern import entity

from assets import Assets
from components.clickable_component import ClickableComponent
from components.gravity_component import GravityComponent
from components.health_component import HealthComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from components.treasure_component import TreasureComponent
from util.additional_math import Vec2
from animation import AnimationComponent, Animation, AnimationFrame


@entity
class BunnyEntity(SpriteComponent, TransformComponent, HitboxComponent, ClickableComponent, GravityComponent,
                  MovementComponent, TileColliderComponent, HealthComponent):

    def serialize(self):
        return BunnyData(self.position)


class BunnyData:
    def __init__(self, position: Vec2):
        self.position = position

    def deserialize(self):
        return BunnyEntity(
            position=self.position,
            width=1,
            height=1,
            health=3,
            speed=Vec2(0, 0),
            acceleration=Vec2(0, 0),
            sprite=Assets.get().bunnyImg,
            hitboxEventHandler=None,
            click_event_handler=None,
            tileBottomLeftRightCollisionEventHandler=None,
            tileTopCollisionEventHandler=None,
        )
