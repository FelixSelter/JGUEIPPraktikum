import pygame
from ecs_pattern import SystemManager
from pygame import Surface
from animation import AnimationSystem
from events import EventParsingSystem, MouseEventName, KeyboardEventName
from map import Map, MapResource
from resources import CameraResource, TimeResource
from scenes import Scene
from systems.click_event_system import ClickEventSystem
from systems.spawner_system import SpawnerSystem
from systems.camera_movement_system import CameraMovementSystem
from systems.entity_collision_system import EntityCollisionSystem
from systems.control_system import ControllerSystem
from systems.gravity_system import GravitySystem
from systems.movement_system import MovementSystem
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem


class GameScene(Scene):
    def __init__(self, screen: Surface):
        super().__init__(screen, None)
        click_event_system = ClickEventSystem(self.entities, None)
        controller_system = ControllerSystem(self.entities, pygame.event.get)

        self.system_manager: SystemManager = SystemManager([
            EventParsingSystem(screen, self.entities, {
                MouseEventName.MouseButtonUp: [click_event_system.click_event_handler],
                MouseEventName.MouseButtonDown: [click_event_system.click_event_handler],
                MouseEventName.MouseDragEnd: [click_event_system.click_event_handler],
                KeyboardEventName.KeyDown: [controller_system.keypress_event_handler],
                KeyboardEventName.KeyUp: [controller_system.keypress_event_handler],
            }),
            TimeSystem(self.entities),
            click_event_system,
            controller_system,
            MovementSystem(self.entities),
            EntityCollisionSystem(self.entities),
            GravitySystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            CameraMovementSystem(self.entities, screen),
            RenderingSystem(self.entities, screen),
            SpawnerSystem(self.entities)
        ])

    def load(self):
        m = Map.load("rsc/Maps/40.map")
        tiles, entities = m.parse()

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
                y=0,
                ui_manager=self.ui_manager
            ),
            MapResource(
                map=m
            ),
            *tiles,
            *entities

        )
