from enum import Enum
from math import copysign
from typing import List

from ecs_pattern import System, EntityManager

from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
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

    def keypress_event_handler(self, event: KeyboardEvent) -> None:
        self.keyboard_events.append(event)

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        for player_entity in self.entities.get_by_class(PlayerEntity):
            player_entity: PlayerEntity = player_entity

            for event in self.keyboard_events:

                # Jumping
                if event.key == player_entity.key_up and event.event_type == KeyboardEventType.KeyDown and player_entity.speed.y == 0:
                    player_entity.speed.y = player_entity.jump

                # Horizontal Controls
                if event.key in player_entity.key_array:
                    player_entity.key_array[event.key] = event.event_type == KeyboardEventType.KeyDown

            # Determine horizontal movement
            horizontal_movement = HorizontalMovementType.NoMovement

            # Stop the player if no or both keys pressed
            if player_entity.key_array[player_entity.key_left] == player_entity.key_array[player_entity.key_right]:
                if not player_entity.speed.x == 0:
                    horizontal_movement = HorizontalMovementType.Decelerate

            # Stop right movement then move left
            elif player_entity.key_array[player_entity.key_left] and not player_entity.key_array[
                player_entity.key_right]:
                player_entity.activeAnimation = "left" if player_entity.last_hit + player_entity.invincibility_time < time_rsc.totalTime else "invincible-left"
                horizontal_movement = HorizontalMovementType.AccelerateLeft if player_entity.speed.x <= 0 else HorizontalMovementType.Decelerate

            # Stop left movement then move right
            elif player_entity.key_array[player_entity.key_right] and not player_entity.key_array[
                player_entity.key_left]:
                player_entity.activeAnimation = "right" if player_entity.last_hit + player_entity.invincibility_time < time_rsc.totalTime else "invincible-right"
                horizontal_movement = HorizontalMovementType.AccelerateRight if player_entity.speed.x >= 0 else HorizontalMovementType.Decelerate

            # Apply horizontal movement
            deceleration = 30
            acceleration = 30

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
                    if abs(player_entity.speed.x) >= player_entity.maxspeed:
                        player_entity.speed.x = -player_entity.maxspeed
                        player_entity.acceleration.x = 0
                    else:
                        player_entity.acceleration.x = -acceleration

                case HorizontalMovementType.AccelerateRight:
                    if abs(player_entity.speed.x) >= player_entity.maxspeed:
                        player_entity.speed.x = player_entity.maxspeed
                        player_entity.acceleration.x = 0
                    else:
                        player_entity.acceleration.x = acceleration

        self.keyboard_events.clear()
