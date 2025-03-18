import time
from typing import List

import pygame
from ecs_pattern import System, EntityManager

from Entities import Tile, PlayerEntity
from Resources import GlobalStateResource, CameraResource, TimeResource, MapResource
from util.math import Vec2


def generate_map(lvl: str) -> [Tile]:
    def create_tile(tile: str, x_cor: float, y_cor: float) -> Tile:
        image = pygame.image.load("rsc/Tiles/" + tile + ".bmp").convert_alpha()
        return Tile(
            position=Vec2(x_cor, y_cor),
            width=1,
            height=1,
            sprite=image
        )

    tile_array: [Tile] = []
    tile_ids: [[str]] = []

    with open("rsc/Maps/" + lvl, 'r') as file:
        lines = file.readlines()

        map_part: bool = False
        for index, line in enumerate(lines):
            line = line.strip()

            if line == "MAP":
                if map_part:
                    break
                else:
                    map_part = True
            else:
                if map_part:
                    tile_ids.append(line.split(" "))

    map_height: int = len(tile_ids)
    solid_tiles: List[List[bool]] = [[] for _ in range(map_height)]  # For Tile collisions
    for i in range(map_height):
        y = map_height - i - 1
        solid_tiles[y] = [False for _ in range(len(tile_ids[i]))]
        for x, tile_id in enumerate(tile_ids[i]):
            if not tile_id == "0":
                tile_array.append(create_tile(tile_id, x, y))
                solid_tiles[y][x] = True

    return tile_array, solid_tiles


class InitSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def start(self):
        tiles, collisionTileMap = generate_map("Level1")

        self.entities.add(
            GlobalStateResource(
                play=True,
                pause=False,
            ),
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
                solidTiles=collisionTileMap
            ),
            *tiles,
            PlayerEntity(
                position=Vec2(3, 8),
                width=1,
                height=1,
                sprite=pygame.image.load("rsc/example.bmp").convert_alpha(),
                acceleration=Vec2(0, 0),
                speed=Vec2(0, 0),
                hitboxEventHandler=lambda _: print("hit"),
                tileCollisionEventHandler=lambda _: None,
            )
        )

    def stop(self):
        pass
