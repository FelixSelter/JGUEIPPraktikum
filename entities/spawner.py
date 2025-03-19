from ecs_pattern import entity

from assets import Assets
from components import SpriteComponent, TransformComponent, NameComponent, SpawnerComponent
from util.math import Vec2


@entity
class SpawnerEntity(SpriteComponent, TransformComponent, NameComponent, SpawnerComponent):
    def serialize(self):
        return SpawnerData(self.position, self.spawnDelay)


class SpawnerData:
    def __init__(self, position: Vec2, spawnDelay: float):
        self.position = position
        self.spawnDelay = spawnDelay

    def deserialize(self) -> SpawnerEntity:
        return SpawnerEntity(
            position=Vec2(6, 3),
            width=1,
            height=1,
            sprite=Assets.get().playerImgs[2],
            name="Cow",
            spawnCounter=0,
            spawnDelay=self.spawnDelay
        )
