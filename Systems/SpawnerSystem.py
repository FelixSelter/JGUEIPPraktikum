from ecs_pattern import System, EntityManager

from Components import SpawnerComponent
from Entities.Enemy import EnemyData
from Resources import TimeResource
from util.math import Vec2


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
                enemy_array.append(EnemyData("Pig", Vec2(8, 4)).deserialize())

        self.entities.add(*enemy_array)
