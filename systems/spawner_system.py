from ecs_pattern import System, EntityManager

from components.spawner_component import SpawnerComponent
from entities.enemy_entity import EnemyData
from resources import TimeResource
from util.additional_math import Vec2
from map import MapResource, Tiles

import random

class SpawnerSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def isTileFree(self, entity):

        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))

        temp_array = [(1, 0), (0, 1), (-1, 0), (0, -1)] # north, east, south, west

        for position in temp_array:
            tile = map_rsc.map.tiles[int(entity.position.y+position[0])][int(entity.position.x+position[1])]
            if tile.isSolid():
                entity.spawnTile.append((0, 0))
            else:
                entity.spawnTile.append(position)

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        enemy_array = []

        for entity in self.entities.get_with_component(SpawnerComponent):
            spawner: SpawnerComponent = entity

            spawner.spawnCounter += time_rsc.deltaTime
            if spawner.spawnCounter >= spawner.spawnDelay:
                spawner.spawnCounter = 0
                if len(spawner.spawnTile) == 4:
                    randomTuple = random.choice(spawner.spawnTile)
                    enemy_array.append(EnemyData(spawner.enemyType, Vec2(entity.position.x+randomTuple[0], entity.position.y+randomTuple[1])).deserialize())
                else:
                    self.isTileFree(entity)

        self.entities.add(*enemy_array)
