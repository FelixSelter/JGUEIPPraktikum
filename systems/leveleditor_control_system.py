from enum import Enum
from math import copysign
from typing import List

from ecs_pattern import System, EntityManager
from pygame import K_w, K_s
from pygame.locals import K_a, K_d, K_SPACE

from components.movement_component import MovementComponent
from entities.player_entity import PlayerEntity
from events import KeyboardEvent, KeyboardEventType
from resources import TimeResource, CameraResource


class LevelEditorControlSystem(System):
    keyboard_events: List[KeyboardEvent] = []
    keys_pressed = {
        K_w: False,
        K_a: False,
        K_s: False,
        K_d: False
    }

    def __init__(self, entities: EntityManager, event_getter):
        self.entities = entities
        self.event_getter = event_getter

    def keypress_event_handler(self, event: KeyboardEvent) -> None:
        self.keyboard_events.append(event)

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        camera_rsc: CameraResource = next(self.entities.get_by_class(CameraResource))

        speed = 3
        for event in self.keyboard_events:
            if event.key in self.keys_pressed:
                self.keys_pressed[event.key] = event.event_type == KeyboardEventType.KeyDown

        if self.keys_pressed[K_w]:
            camera_rsc.y += speed * time_rsc.deltaTime
        if self.keys_pressed[K_a]:
            camera_rsc.x -= speed * time_rsc.deltaTime
        if self.keys_pressed[K_s]:
            camera_rsc.y -= speed * time_rsc.deltaTime
        if self.keys_pressed[K_d]:
            camera_rsc.x += speed * time_rsc.deltaTime

        if camera_rsc.x < 0:
            camera_rsc.x = 0
        if camera_rsc.y < 0:
            camera_rsc.y = 0

        self.keyboard_events.clear()
