from ecs_pattern import System, EntityManager

from components.spawner_component import SpawnerComponent
from entities.enemy_entity import EnemyData
from resources import TimeResource
from util.additional_math import Vec2


class SpawnerSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        enemy_array = []

        for entity in self.entities.get_with_component(SpawnerComponent):
            spawner: SpawnerComponent = entity

            spawner.spawnCounter += time_rsc.deltaTime
            if spawner.spawnCounter >= spawner.spawnDelay:
                spawner.spawnCounter = 0
                enemy_array.append(EnemyData(spawner.enemyType.value, Vec2(entity.position.x-1, entity.position.y)).deserialize())

        self.entities.add(*enemy_array)
