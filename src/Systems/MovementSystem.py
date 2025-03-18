from ecs_pattern import System, EntityManager

from src.Components import TransformComponent, MovementComponent
from src.Resources import TimeResource


class MovementSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for entity in self.entities.get_with_component(MovementComponent, TransformComponent):
            movement: MovementComponent = entity
            transform: TransformComponent = entity

            movement.speed += movement.acceleration * time_rsc.deltaTime
            transform.position += movement.speed * time_rsc.deltaTime
