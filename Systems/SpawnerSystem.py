from ecs_pattern import System, EntityManager

from Components import SpawnerComponent
from Enemy import EnemyEntity
from Resources import TimeResource


class SpawnerSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        enemy_array=[]

        for entity in self.entities.get_with_component(SpawnerComponent):
            entity.counter += time_rsc.deltaTime
            if entity.counter >= 5:
                entity.counter = 0
                test=EnemyEntity.createEnemy("Pig", 8, 4)
                enemy_array.append(test)
        
        self.entities.add(*enemy_array)
