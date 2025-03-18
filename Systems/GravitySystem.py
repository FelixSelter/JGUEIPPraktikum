from typing import List

from ecs_pattern import System, EntityManager

from Components import TransformComponent, HitboxComponent, GravityComponent, MovementComponent
from Resources import MapResource


class GravitySystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        for entity in self.entities.get_with_component(GravityComponent, MovementComponent):
            movement: MovementComponent = entity

            movement.acceleration.y = -30
