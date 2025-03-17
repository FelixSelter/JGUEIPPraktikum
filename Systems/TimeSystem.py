import time
from typing import Iterator, List, Any

import pygame.transform
from ecs_pattern import System, EntityManager
from pygame import Surface

from Components import SpriteComponent, TransformComponent, MovementComponent
from Resources import CameraResource, TimeResource
from util import requireAll


class TimeSystem(System):
    last_time = time.time()

    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        if not time_rsc.paused:
            t = time.time()
            time_rsc.deltaTime = t - self.last_time
            time_rsc.totalTime += time_rsc.deltaTime
            self.last_time = t
        elif time_rsc.doUnPause:
            self.last_time = time.time()
            time_rsc.paused = False
            time_rsc.doUnPause = False
