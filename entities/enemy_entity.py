from enum import Enum

from assets import Assets
from components.gravity_component import GravityComponent
from components.health_component import HealthComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.name_component import NameComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from util import CollisionDirection
from util.additional_math import Vec2
from ecs_pattern import EntityManager, entity
from animation import AnimationComponent, Animation, AnimationFrame


class EnemyType(Enum):
    Cow = "Cow"
    Pig = "Pig"
    Sheep = "Sheep"


@entity
class EnemyEntity(SpriteComponent, TransformComponent, HitboxComponent, TileColliderComponent, GravityComponent,
                  MovementComponent, NameComponent, AnimationComponent, HealthComponent):
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
        # enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.activeAnimation = "walking_left"
        enemy.speed.x = -EnemyEntity.animals_dict[enemy.name]
    elif direction == CollisionDirection.Right:
        # enemy.sprite = pygame.transform.flip(enemy.sprite, True, False)
        enemy.activeAnimation = "walking_right"
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
            health=1,
            sprite=Assets.get().enemyImgsDict[self.name][0][0],
            acceleration=Vec2(0, 0),
            speed=Vec2(-EnemyEntity.animals_dict[self.name], 0),
            tileBottomLeftRightCollisionEventHandler=enemyCollisionHandler,
            tileTopCollisionEventHandler=None,
            hitboxEventHandler=None,
            animations={
                "walking_left": Animation(
                    [AnimationFrame(Assets.get().enemyImgsDict[self.name][0][i], 0.1) for i in
                     range(len(Assets.get().enemyImgsDict[self.name][0]))]),
                "walking_right": Animation(
                    [AnimationFrame(Assets.get().enemyImgsDict[self.name][1][i], 0.1) for i in
                     range(len(Assets.get().enemyImgsDict[self.name][1]))])},
            activeAnimation="walking_left",
            currentTime=0,
            loopAnimation=True
        )
