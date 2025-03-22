from typing import List

import pygame
from ecs_pattern import System, EntityManager

from components.clickable_component import ClickableComponent
from components.hitbox_component import HitboxComponent
from components.transform_component import TransformComponent
from entities.player_entity import PlayerEntity
from events import MouseEvent, MouseEventType
from resources import CameraResource


class ClickEventSystem(System):
    mouse_events: List[MouseEvent] = []

    def __init__(self, entities: EntityManager):
        self.entities = entities

        # Unnecessarily iterating over events multiple times
        # Getting the tile from a position efficiently
        # Clicks into space where no entity is

        # Event system parses pygame events once
        # Calls the required handlers
        # event bubbling and cancellation. If a sprite has been clicked we dont check for tiles if a tile has been clicked we dont check for space
        # Tiles register themself upon creation

    def click_event_handler(self, event: MouseEvent) -> None:
        self.mouse_events.append(event)

    def update(self):
        for mouse_event in self.mouse_events:
            if not mouse_event.event_type == MouseEventType.Released:
                continue

            # Check if an entity has been clicked
            for entity in self.entities.get_with_component(ClickableComponent, HitboxComponent, TransformComponent):
                transform: TransformComponent = entity
                clickable: ClickableComponent = entity
                if 0 < mouse_event.world_start_pos.x - transform.position.x < transform.width and 0 < mouse_event.world_end_pos.y - transform.position.y < transform.height:
                    mouse_event.canceled = True
                    if clickable.click_event_handler is not None:
                        clickable.click_event_handler(entity)
                    break

            # Dont continue searching if we already found an entity
            if mouse_event.canceled:
                break

        self.mouse_events.clear()
