from typing import Any

import pygame
from ecs_pattern import SystemManager
from pygame import Surface

from Animation import AnimationSystem
from Map import Map, MapResource
from Resources import CameraResource, TimeResource
from Scenes import Scene
from Systems.SpawnerSystem import SpawnerSystem
from Systems.CameraMovementSystem import CameraMovementSystem
from Systems.CollisionSystem import CollisionSystem
from Systems.ControlSystem import ControllerSystem
from Systems.GravitySystem import GravitySystem
from Systems.MovementSystem import MovementSystem
from Systems.PurgeDeleteBufferSystem import PurgeDeleteBufferSystem
from Systems.RenderingSystem import RenderingSystem
from Systems.TileCollisionSystem import TileCollisionSystem
from Systems.TimeSystem import TimeSystem


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
