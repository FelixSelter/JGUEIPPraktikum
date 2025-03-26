from random import choice

from ecs_pattern import entity, EntityManager

from assets import Assets
from components.clickable_component import ClickableComponent
from components.hitbox_component import HitboxComponent
from components.spawner_component import SpawnerComponent
from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent
from entities.enemy_entity import EnemyType, EnemyData
from map import MapResource
from timed_action import TimedActionComponent, TimedAction
from util.additional_math import Vec2


@entity
class SpawnerEntity(SpriteComponent, TransformComponent, SpawnerComponent, ClickableComponent, HitboxComponent,
                    TimedActionComponent):
    def serialize(self):
        return SpawnerData(self.position, self.spawnDelay, self.enemyType)


class SpawnAction(TimedAction):
    def __init__(self, spawn_delay: float):
        super().__init__(attack_delay=spawn_delay)

    def isTileFree(self, entity: SpawnerEntity, entities: EntityManager):

        map_rsc: MapResource = next(entities.get_by_class(MapResource))

        temp_array = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # north, east, south, west

        for position in temp_array:
            tile = map_rsc.map.tiles[int(entity.position.y + position[0])][int(entity.position.x + position[1])]
            if tile.isSolid():
                entity.spawnTile.append((0, 0))
            else:
                entity.spawnTile.append(position)

    def execute_action(self, spawner: SpawnerEntity, entities: EntityManager):
        if len(spawner.spawnTile) == 4:
            randomTuple = choice(spawner.spawnTile)
            entities.add_buffer.append(EnemyData(spawner.enemyType.value, Vec2(spawner.position.x + randomTuple[0],
                                                                               spawner.position.y + randomTuple[
                                                                                   1])).deserialize())
        else:
            self.isTileFree(spawner, entities)


class SpawnerData:
    def __init__(self, position: Vec2, spawnDelay: float, enemyType: EnemyType):
        self.position = position
        self.spawnDelay = spawnDelay
        self.enemyType = enemyType

    def deserialize(self) -> SpawnerEntity:
        return SpawnerEntity(
            position=self.position,
            width=1,
            height=1,
            sprite=Assets.get().spawnerImg[self.enemyType if isinstance(self.enemyType, str) else self.enemyType.name],
            spawnCounter=0,
            spawnDelay=self.spawnDelay,
            enemyType=self.enemyType,
            hitboxEventHandler=None,
            click_event_handler=None,
            actions=[SpawnAction(self.spawnDelay)],
            spawnTile=[]
        )
