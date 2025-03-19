from typing import Any, List

import pygame
from ecs_pattern import SystemManager, EntityManager
from pygame import Surface

from Entities import CoinEntity, PlayerEntity, Tile
from Resources import MapResource, CameraResource, TimeResource
from Scenes import Scene
from Systems.CollisionSystem import CollisionSystem
from Systems.ControlSystem import ControllerSystem
from Systems.GravitySystem import GravitySystem
from Systems.MovementSystem import MovementSystem
from Systems.PurgeDeleteBufferSystem import PurgeDeleteBufferSystem
from Systems.RenderingSystem import RenderingSystem
from Systems.TileCollisionSystem import TileCollisionSystem
from Systems.TimeSystem import TimeSystem
from Assets import Assets
from util.math import Vec2


def playerCollisionHandler(player: PlayerEntity, item: Any, entities: EntityManager):
    if isinstance(item, CoinEntity):
        player.score += item.treasure
        entities.delete_buffer_add(item)


def generate_map(lvl: str) -> [Tile]:
    def create_tile(tile: str, x_cor: float, y_cor: float) -> Tile:
        image = Assets.get().tileImgs[tile]
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


class GameScene(Scene):
    def __init__(self, screen: Surface):
        self.system_manager: SystemManager = SystemManager([
            TimeSystem(self.entities),
            ControllerSystem(self.entities, pygame.event.get),
            GravitySystem(self.entities),
            MovementSystem(self.entities),
            TileCollisionSystem(self.entities),
            CollisionSystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            RenderingSystem(self.entities, screen)
        ])

    def load(self):
        tiles, collisionTileMap = generate_map("Level1")

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
                solidTiles=collisionTileMap
            ),
            *tiles,
            PlayerEntity(
                position=Vec2(3, 8),
                width=1,
                height=1,
                sprite=Assets.get().playerImg,
                acceleration=Vec2(0, 0),
                speed=Vec2(0, 0),
                hitboxEventHandler=playerCollisionHandler,
                tileCollisionEventHandler=lambda _a, _b: None,
                score=0
            ),
            CoinEntity(
                position=Vec2(5.25, 3.25),
                width=0.5,
                height=0.5,
                sprite=Assets.get().coinImg,
                hitboxEventHandler=lambda _a, _b, _c: None,
                treasure=1
            )
        )
