from enum import Enum

import pygame
from assets import Assets
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.name_component import NameComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from util import CollisionDirection
from util.additional_math import Vec2
from ecs_pattern import EntityManager, entity


class EnemyType(Enum):
    Cow = "Cow"
    Pig = "Pig"
    Sheep = "Sheep"


@entity
class EnemyEntity(SpriteComponent, TransformComponent, HitboxComponent, TileColliderComponent, GravityComponent,
                  MovementComponent, NameComponent):
    animals_dict = {
        "Cow": 3,
        "Pig": 2,
        "Sheep": 1
    }

    def serialize(self):
        return EnemyData(self.name, self.position)


def enemyCollisionHandler(enemy: EnemyEntity, direction: CollisionDirection, tile: (int, int),
                          entities: EntityManager):
    if direction == CollisionDirection.Left:
        enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.speed.x = -EnemyEntity.animals_dict[enemy.name]
    elif direction == CollisionDirection.Right:
        enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
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
            sprite=Assets.get().enemyImg_pig,
            acceleration=Vec2(0, 0),
            speed=Vec2(-EnemyEntity.animals_dict[self.name], 0),
            tileBottomLeftRightCollisionEventHandler=enemyCollisionHandler,
            tileTopCollisionEventHandler=None,
            hitboxEventHandler=None
        )
