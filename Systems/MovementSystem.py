from typing import Iterator, List, Any

import pygame.transform
from ecs_pattern import System, EntityManager
from pygame import Surface

from Components import SpriteComponent, TransformComponent, MovementComponent
from Resources import CameraResource, TimeResource
from util import requireAll


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
