from dataclasses import dataclass
from enum import Enum

import pygame
from ecs_pattern import EntityManager
from pygame import Surface

from events import Event
from resources import CameraResource


# Events emitted by the event system
class MouseEventName(Enum):
    MouseButtonDown = "MouseButtonDown"
    MouseDragEnd = "MouseDragEnd"
    MouseButtonUp = "MouseButtonUp"


class MouseEventType(Enum):
    Pressed = 0
    Released = 1
    DragEnd = 2


class MouseButton(Enum):
    Left = 0
    Right = 2
    Middle = 1


class MouseEvent(Event):
    def __init__(self, screen: Surface, entities: EntityManager, button: MouseButton, event_type: MouseEventType,
                 px_start_pos: (int, int),
                 px_end_pos: (int, int)):
        self.button = button
        self.event_type = event_type
        self.start_pos = px_start_pos
        self.end_pos = px_end_pos

        # Calculate world position
        camera: CameraResource = next(entities.get_by_class(CameraResource))

        screen_width, screen_height = screen.get_size()
        tile_width = screen_width / camera.screenWidthInTiles
        tile_height = screen_height / camera.screenHeightInTiles

        def px_to_world_pos(px_x: int, px_y: int):
            x = px_x / tile_width
            y = (screen_height - px_y) / tile_height  # Invert y
            return x + camera.x, y + camera.y

        self.world_start_pos = px_to_world_pos(*px_start_pos)
        self.world_end_pos = px_to_world_pos(*px_end_pos)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"button={self.button}, event_type={self.event_type}, "
                f"start_pos={self.start_pos}, end_pos={self.end_pos}, "
                f"world_start_pos={self.world_start_pos}, world_end_pos={self.world_end_pos})")
