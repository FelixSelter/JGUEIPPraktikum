import pygame
from assets import Assets
from components import NameComponent, GravityComponent, HitboxComponent, MovementComponent, SpriteComponent, \
    TileColliderComponent, TileCollisionDirection, TransformComponent
from util.math import Vec2
from ecs_pattern import EntityManager, entity


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


def enemyCollisionHandler(enemy: EnemyEntity, direction: TileCollisionDirection, entities: EntityManager):
    if direction == TileCollisionDirection.Left:
        enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.speed.x = -EnemyEntity.animals_dict[enemy.name]
    elif direction == TileCollisionDirection.Right:
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
            tileCollisionEventHandler=enemyCollisionHandler,
            hitboxEventHandler=lambda _a, _b, _c: None
        )
