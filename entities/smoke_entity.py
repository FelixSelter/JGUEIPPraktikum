from random import choice

from ecs_pattern import entity, EntityManager

from animation import AnimationComponent
from assets import Assets
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from entities.enemy_entity import EnemyData
from timed_action import TimedActionComponent, TimedAction


@entity
class SmokeEntity(SpriteComponent, TransformComponent, AnimationComponent, TimedActionComponent):
    pass


class SmokeDeleteAction(TimedAction):

    def __init__(self):
        super().__init__(attack_delay=0.5, executed_immediate=False)

    def execute_action(self, smoke: SmokeEntity, entities: EntityManager):
        entities.delete_buffer_add(smoke)
