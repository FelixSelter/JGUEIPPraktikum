from random import choice

from ecs_pattern import entity, EntityManager

from assets import Assets
from components.clickable_component import ClickableComponent
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from components.treasure_component import TreasureComponent
from entities.enemy_entity import EnemyData
from resources import TimeResource
from timed_action import TimedActionComponent, TimedAction
from util.additional_math import Vec2
from animation import AnimationComponent, Animation, AnimationFrame


@entity
class BunnyEggEntity(SpriteComponent, TransformComponent, HitboxComponent, MovementComponent, GravityComponent,
                     TileColliderComponent, TimedActionComponent):
    pass


class BunnyEggAction(TimedAction):
    def __init__(self):
        super().__init__(attack_delay=1.5)

    def execute_action(self, egg: BunnyEggEntity, entities: EntityManager):
        entities.delete_buffer_add(egg)
        entities.add_buffer.append(
            EnemyData(choice([name for name in Assets.get().enemyImgsDict.keys()]), egg.position).deserialize())
