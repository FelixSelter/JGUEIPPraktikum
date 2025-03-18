from typing import List

import pygame
from ecs_pattern import entity


@entity
class GlobalStateResource:
    play: bool
    pause: bool


@entity
class MapResource:
    solidTiles: List[List[bool]]  # For collisions solidTiles[y/row][x/col]


@entity
class TimeResource:
    totalTime: float
    deltaTime: float
    doUnPause: bool
    paused: bool


@entity
class CameraResource:
    screenWidthInTiles: int  # number of tiles visible on screen
    screenHeightInTiles: int  # number of tiles visible on screen
    x: float  # In tile coordinates
    y: float  # In tile coordinates
