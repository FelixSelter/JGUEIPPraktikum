import pygame
from ecs_pattern import SystemManager
from pygame import Surface

from animation import AnimationSystem
from map import Map, MapResource
from resources import CameraResource, TimeResource
from Scenes import Scene
from Systems.spawner_system import SpawnerSystem
from Systems.camera_movement_system import CameraMovementSystem
from Systems.collision_system import CollisionSystem
from Systems.control_system import ControllerSystem
from Systems.gravity_system import GravitySystem
from Systems.movement_system import MovementSystem
from Systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from Systems.rendering_system import RenderingSystem
from Systems.tile_collision_system import TileCollisionSystem
from Systems.time_system import TimeSystem


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
