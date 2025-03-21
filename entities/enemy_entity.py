from enum import Enum

import pygame
from assets import Assets
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.name_component import NameComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent, TileCollisionDirection
from components.transform_component import TransformComponent
from util.math import Vec2
from ecs_pattern import EntityManager, entity
from animation import AnimationComponent, Animation, AnimationFrame

class EnemyType(Enum):
    Cow = "Cow"
    Pig = "Pig"
    Sheep = "Sheep"


@entity
class EnemyEntity(SpriteComponent, TransformComponent, HitboxComponent, TileColliderComponent, GravityComponent,
                  MovementComponent, NameComponent, AnimationComponent):
    animals_dict = {
        "Cow": 3,
        "Pig": 2,
        "Sheep": 1
    }

    def serialize(self):
        return EnemyData(self.name, self.position)


def enemyCollisionHandler(enemy: EnemyEntity, direction: TileCollisionDirection, entities: EntityManager):
    if direction == TileCollisionDirection.Left:
        #enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.activeAnimation="walking_left"
        enemy.speed.x = -EnemyEntity.animals_dict[enemy.name]
    elif direction == TileCollisionDirection.Right:
        #enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.activeAnimation="walking_right"
        enemy.speed.x = EnemyEntity.animals_dict[enemy.name]


class EnemyData:
    def __init__(self, name: str, position: Vec2):
        self.name = name
        self.position = position

    def deserialize(self):
        return EnemyEntity(
            name=self.name,
            position=self.position,
            width=1,
            height=1,
            sprite=Assets.get().enemyImgs_pig_left[0],
            acceleration=Vec2(0, 0),
            speed=Vec2(-EnemyEntity.animals_dict[self.name], 0),
            tileCollisionEventHandler=enemyCollisionHandler,
            hitboxEventHandler=None,
            animations={
                "walking_left": Animation(
                [AnimationFrame(Assets.get().enemyImgs_pig_left[0], 0.1), AnimationFrame(Assets.get().enemyImgs_pig_left[1], 0.1)]),
                "walking_right": Animation(
                [AnimationFrame(Assets.get().enemyImgs_pig_right[0], 0.1), AnimationFrame(Assets.get().enemyImgs_pig_right[1], 0.1)])},
            activeAnimation="walking_left",
            currentTime=0,
            loopAnimation=True
        )
