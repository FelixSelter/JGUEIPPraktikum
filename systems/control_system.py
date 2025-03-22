from enum import Enum
from math import copysign
from typing import List

from ecs_pattern import System, EntityManager
from pygame.locals import K_a, K_d, K_SPACE

from components.movement_component import MovementComponent
from entities.player_entity import PlayerEntity
from events import KeyboardEvent, KeyboardEventType
from resources import TimeResource


class HorizontalMovementType(Enum):
    AccelerateLeft = 0
    AccelerateRight = 1
    Decelerate = 2
    NoMovement = 3


class ControllerSystem(System):
    keyboard_events: List[KeyboardEvent] = []

    def __init__(self, entities: EntityManager, event_getter):
        self.entities = entities
        self.event_getter = event_getter

        self.movement_keys = {K_a: False, K_d: False}

    def keypress_event_handler(self, event: KeyboardEvent) -> None:
        self.keyboard_events.append(event)

    def update(self):
        for player_entity in self.entities.get_by_class(PlayerEntity):
            player_entity: MovementComponent = player_entity
            time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

            for event in self.keyboard_events:
                # Jumping
                if event.key == K_SPACE and event.event_type == KeyboardEventType.KeyDown and player_entity.speed.y == 0:
                    player_entity.speed.y = 15

                # Horizontal Controls
                if event.key in self.movement_keys:
                    self.movement_keys[event.key] = event.event_type == KeyboardEventType.KeyDown

            self.keyboard_events.clear()

            # Determine horizontal movement
            horizontal_movement = HorizontalMovementType.NoMovement

            # Stop the player if no or both keys pressed
            if self.movement_keys[K_a] == self.movement_keys[K_d]:
                if not player_entity.speed.x == 0:
                    horizontal_movement = HorizontalMovementType.Decelerate

            # Stop right movement then move left
            elif self.movement_keys[K_a] and not self.movement_keys[K_d]:
                horizontal_movement = HorizontalMovementType.AccelerateLeft if player_entity.speed.x <= 0 else HorizontalMovementType.Decelerate

            # Stop left movement then move right
            elif self.movement_keys[K_d] and not self.movement_keys[K_a]:
                horizontal_movement = HorizontalMovementType.AccelerateRight if player_entity.speed.x >= 0 else HorizontalMovementType.Decelerate

            # Apply horizontal movement
            deceleration = 30
            acceleration = 30
            maxSpeed = 10

            player_entity.acceleration.x = 0
            match horizontal_movement:
                case HorizontalMovementType.NoMovement:
                    pass

                case HorizontalMovementType.Decelerate:
                    requiredStopAcceleration = -player_entity.speed.x / time_rsc.deltaTime
                    if abs(requiredStopAcceleration) <= deceleration:  # If can fully stop do that
                        player_entity.speed.x = 0
                    else:  # Continue decelerating
                        player_entity.acceleration.x = copysign(deceleration,
                                                                requiredStopAcceleration)  # apply max deceleration in the correct direction

                case HorizontalMovementType.AccelerateLeft:
                    if abs(player_entity.speed.x) >= maxSpeed:
                        player_entity.speed.x = -maxSpeed
                        player_entity.acceleration.x = 0
                    else:
                        player_entity.acceleration.x = -acceleration

                case HorizontalMovementType.AccelerateRight:
                    if abs(player_entity.speed.x) >= maxSpeed:
                        player_entity.speed.x = maxSpeed
                        player_entity.acceleration.x = 0
                    else:
                        player_entity.acceleration.x = acceleration
