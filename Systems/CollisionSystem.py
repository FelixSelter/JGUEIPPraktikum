from typing import List

from ecs_pattern import System, EntityManager

from Components import TransformComponent, HitboxComponent


class CollisionSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        entities: List[TransformComponent] = list(self.entities.get_with_component(HitboxComponent, TransformComponent))
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                obj1: TransformComponent = entities[i]
                obj2: TransformComponent = entities[j]

                if obj1.position.x + obj1.width >= obj2.position.x and \
                        obj1.position.x <= obj2.position.x + obj2.width and \
                        obj1.position.y + obj1.height >= obj2.position.y and \
                        obj1.position.y <= obj2.position.y + obj2.height:
                    obj1: HitboxComponent = obj1
                    obj1.hitboxEventHandler(obj1, obj2, self.entities)
                    obj2: HitboxComponent = obj2
                    obj2.hitboxEventHandler(obj1, obj2, self.entities)
