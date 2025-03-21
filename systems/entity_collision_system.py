from typing import List

from ecs_pattern import System, EntityManager

from components.hitbox_component import HitboxComponent
from components.transform_component import TransformComponent
from util import CollisionDirection


class EntityCollisionSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        entities: List[TransformComponent] = list(self.entities.get_with_component(HitboxComponent, TransformComponent))
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                obj1: TransformComponent = entities[i]
                obj2: TransformComponent = entities[j]

                right_edge_right_of_left_edge = obj1.position.x + obj1.width >= obj2.position.x
                left_edge_not_right_of_right_edge = obj1.position.x <= obj2.position.x + obj2.width
                top_edge_above_bottom_edge = obj1.position.y + obj1.height >= obj2.position.y
                bottom_edge_not_above_top_edge = obj1.position.y <= obj2.position.y + obj2.height

                if right_edge_right_of_left_edge and \
                        left_edge_not_right_of_right_edge and \
                        top_edge_above_bottom_edge and \
                        bottom_edge_not_above_top_edge:

                    # Possible collision to the left edge of obj2
                    left_edge_left_of_left_edge = obj1.position.x < obj2.position.x

                    # Possible collision to the bottom edge of obj2
                    bottom_edge_below_bottom_edge = obj1.position.y < obj2.position.y

                    overlap_x = min(obj1.position.x + obj1.width, obj2.position.x + obj2.width) - max(obj1.position.x,
                                                                                                      obj2.position.x)
                    overlap_y = min(obj1.position.y + obj1.height, obj2.position.y + obj2.height) - max(obj1.position.y,
                                                                                                        obj2.position.y)
                    assert overlap_x >= 0 and overlap_y >= 0

                    if overlap_x < overlap_y:
                        collision_direction = CollisionDirection.Left if left_edge_left_of_left_edge else CollisionDirection.Right
                    else:
                        collision_direction = CollisionDirection.Bottom if bottom_edge_below_bottom_edge else CollisionDirection.Top

                    obj1: HitboxComponent = obj1
                    if obj1.hitboxEventHandler is not None:
                        obj1.hitboxEventHandler(obj1, obj2, collision_direction, self.entities)
                    obj2: HitboxComponent = obj2
                    if obj2.hitboxEventHandler is not None:
                        obj2.hitboxEventHandler(obj1, obj2, collision_direction.mirror(), self.entities)
