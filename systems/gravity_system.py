from ecs_pattern import System, EntityManager

from components.gravity_component import GravityComponent
from components.movement_component import MovementComponent


class GravitySystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        for entity in self.entities.get_with_component(GravityComponent, MovementComponent):
            movement: MovementComponent = entity

            movement.acceleration.y = -31
