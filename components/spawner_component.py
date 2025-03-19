from ecs_pattern import component

from entities.enemy_entity import EnemyType


@component
class SpawnerComponent:
    spawnCounter: float
    spawnDelay: float
    enemyType: EnemyType
