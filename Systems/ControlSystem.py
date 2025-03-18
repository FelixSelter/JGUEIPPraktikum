from enum import Enum
from math import copysign

import pygame, sys
from ecs_pattern import System, EntityManager
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_a, K_d, K_SPACE

from Components import MovementComponent
from Resources import GlobalStateResource, TimeResource
from Entities import PlayerEntity


class HorizontalMovementType(Enum):
    AccelerateLeft = 0
    AccelerateRight = 1
    Decelerate = 2
    NoMovement = 3


class ControllerSystem(System):
    def __init__(self, entities: EntityManager, event_getter):
        self.entities = entities
        self.event_getter = event_getter

        self.movement_keys = {K_a: False, K_d: False}

    def start(self):
        pass

    def calculate_acceleration(self, speed):
        pass

    def update(self):
        player_entity: MovementComponent = next(self.entities.get_by_class(PlayerEntity))
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for event in self.event_getter():
            event_type = event.type
            event_key = getattr(event, 'key', None)
            game_state_info = next(self.entities.get_by_class(GlobalStateResource))

            # Quit game
            if event_type == QUIT:
                game_state_info.play = False
                sys.exit()

            # Pause game
            if event_key == K_ESCAPE:
                pygame.quit()
                game_state_info.play = False
                sys.exit()

            # Jumping
            if event_key == K_SPACE:
                if event_type == KEYDOWN and player_entity.speed.y == 0:
                    player_entity.speed.y = 15

            # Horizontal Controls
            if event_key in self.movement_keys:
                self.movement_keys[event_key] = event_type == KEYDOWN

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
        maxSpeed = 15

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
