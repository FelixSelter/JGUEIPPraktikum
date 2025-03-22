from typing import List

import pygame
from ecs_pattern import System, EntityManager

from components.clickable_component import ClickableComponent
from events import MouseEvent
from resources import CameraResource


class HitBoxComponent:
    pass


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
            print(mouse_event)

            # Check if an entity has been clicked
            for entity in self.entities.get_with_component(ClickableComponent, HitBoxComponent):
                pass

            # Check if a tile has been clicked

        self.mouse_events.clear()
