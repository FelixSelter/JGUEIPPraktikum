from ecs_pattern import component

from entities.enemy_entity import EnemyType
from typing import List

@component
class SpawnerComponent:
    spawnCounter: float
    spawnDelay: float
    enemyType: EnemyType
    spawnTile: List[tuple[int, int]] # maximal 4 integers (north, east, south, west)
