import pygame
from Assets import Assets
from Components import NameComponent, GravityComponent, HitboxComponent, MovementComponent, SpriteComponent, \
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

    @staticmethod
    def createEnemy(enemyName: str, x: float, y: float):
        return EnemyEntity(
            enemyName=enemyName,
            position=Vec2(x, y),
            width=1,
            height=1,
            sprite=Assets.get().enemyImg_pig,
            acceleration=Vec2(0, 0),
            speed=Vec2(EnemyEntity.animals_dict[enemyName], 0),
            tileCollisionEventHandler=enemyCollisionHandler,
            hitboxEventHandler=lambda _a, _b, _c: None
        )


def enemyCollisionHandler(enemy: EnemyEntity, direction: TileCollisionDirection, entities: EntityManager):
    if direction == TileCollisionDirection.Left:
        enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.speed.x = -EnemyEntity.animals_dict[enemy.name]
    elif direction == TileCollisionDirection.Right:
        enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.speed.x = EnemyEntity.animals_dict[enemy.name]
