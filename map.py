import pickle
from enum import Enum
from typing import List

from ecs_pattern import entity

from assets import Assets
from entities.tile_entity import TileEntity
from util.math import Vec2


class Tiles(Enum):
    Air = ""
    Dirt = "dirt"
    Dirt2 = "dirt2"
    DirtBottom = "dirt-bottom"
    DirtLeft = "dirt-left"
    DirtLeftCorner = "dirt-left-corner"
    DirtRight = "dirt-right"
    DirtRightCorner = "dirt-right-corner"
    Grass = "grass"
    GrassLeft = "grass-left"
    GrassRight = "grass-right"
    Hay = "hay"

    def getSprite(self):
        if self == Tiles.Air:
            raise Exception("Tried to get the sprite of air")
        return Assets.get().tileImgs[self.value]

    def isSolid(self):
        return not self == Tiles.Air


class Map:
    def __init__(self, tiles: List[List[Tiles]], entityData: List):
        self.tiles = tiles  # [row][col]
        self.height = len(tiles)
        self.width = len(tiles[0])
        self.entityData = entityData

    def save(self, path: str):
        with open(path, "wb") as outfile:
            pickle.dump(self, outfile)

    @staticmethod
    def load(path: str):
        with open(path, "rb") as infile:
            return pickle.load(infile)

    def parse(self):
        tiles = []

        for rowIndex, row in enumerate(self.tiles):
            for colIndex, tile in enumerate(row):
                if tile == Tiles.Air:
                    continue
                tiles.append(TileEntity(
                    position=Vec2(colIndex, rowIndex),
                    width=1,
                    height=1,
                    sprite=tile.getSprite()
                ))

        entities = [entity.deserialize() for entity in self.entityData]

        return tiles, entities


@entity
class MapResource:
    map: Map
