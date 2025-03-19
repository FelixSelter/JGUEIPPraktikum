from typing import Any

import pygame
from ecs_pattern import SystemManager
from pygame import Surface

from animation import AnimationSystem
from map import Map, MapResource
from resources import CameraResource, TimeResource
from Scenes import Scene
from systems.spawner_system import SpawnerSystem
from systems.camera_movement_system import CameraMovementSystem
from systems.collision_system import CollisionSystem
from systems.control_system import ControllerSystem
from systems.gravity_system import GravitySystem
from systems.movement_system import MovementSystem
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.tile_collision_system import TileCollisionSystem
from systems.time_system import TimeSystem


class GameScene(Scene):
    def __init__(self, screen: Surface):
        self.system_manager: SystemManager = SystemManager([
            TimeSystem(self.entities),
            ControllerSystem(self.entities, pygame.event.get),
            MovementSystem(self.entities),
            TileCollisionSystem(self.entities),
            CollisionSystem(self.entities),
            GravitySystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            CameraMovementSystem(self.entities, screen),
            RenderingSystem(self.entities, screen),
            SpawnerSystem(self.entities)
        ])

    def load(self):
        m = Map.load("rsc/Maps/Level1")
        tiles, entities = m.parse()

        self.entities.add(
            TimeResource(
                totalTime=0,
                deltaTime=0,
                paused=False,
                doUnPause=False,
            ),
            CameraResource(
                screenWidthInTiles=16,
                screenHeightInTiles=9,
                x=0,
                y=0
            ),
            MapResource(
                map=m
            ),
            *tiles,
            *entities

        )
