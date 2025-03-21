from ecs_pattern import entity

from assets import Assets
from components.name_component import NameComponent
from components.spawner_component import SpawnerComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from entities.enemy_entity import EnemyType
from util.math import Vec2


@entity
class SpawnerEntity(SpriteComponent, TransformComponent, SpawnerComponent):
    def serialize(self):
        return SpawnerData(self.position, self.spawnDelay, self.enemyType)


class SpawnerData:
    def __init__(self, position: Vec2, spawnDelay: float, enemyType: EnemyType):
        self.position = position
        self.spawnDelay = spawnDelay
        self.enemyType = enemyType

    def deserialize(self) -> SpawnerEntity:
        return SpawnerEntity(
            position=Vec2(6, 3),
            width=1,
            height=1,
            sprite=Assets.get().playerImgs[2],
            spawnCounter=0,
            spawnDelay=self.spawnDelay,
            enemyType=self.enemyType
        )
