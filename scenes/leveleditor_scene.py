import pygame
from ecs_pattern import SystemManager
from pygame import Surface
from animation import AnimationSystem
from entities.coin_entity import CoinData
from events import EventParsingSystem, MouseEventName, KeyboardEventName
from map import Map, MapResource
from resources import CameraResource, TimeResource
from scenes import Scene
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem
from util.additional_math import Vec2


class LevelEditorScene(Scene):
    def __init__(self, screen: Surface):
        self.system_manager: SystemManager = SystemManager([
            EventParsingSystem(screen, self.entities, {
                MouseEventName.MouseButtonUp: [],
                MouseEventName.MouseButtonDown: [],
                MouseEventName.MouseDragEnd: [],
                KeyboardEventName.KeyDown: [],
                KeyboardEventName.KeyUp: [],
            }),
            TimeSystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            RenderingSystem(self.entities, screen)
        ])

    def load(self):
        m = Map([], [])

        self.entities.add(
            TimeResource(
                totalTime=0,
                deltaTime=0,
                paused=False,
                doUnPause=False,
            ),
            CameraResource(
                screenWidthInTiles=16 * 2,
                screenHeightInTiles=9 * 2,
                x=0,
                y=0
            ),
            MapResource(
                map=m
            ),
            CoinData(Vec2(2, 2), 0).deserialize()
        )
