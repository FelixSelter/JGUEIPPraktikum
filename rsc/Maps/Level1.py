import os

from entities.coin_entity import CoinData
from entities.enemy_entity import EnemyType
from entities.player_entity import PlayerData
from entities.spawner_entity import SpawnerData
from map import Tiles, Map
from util.additional_math import Vec2

if __name__ == "__main__":
    name = "Level1"
    if os.path.exists(name):
        os.remove(name)

    tiles = [
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Dirt, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.GrassLeft, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass,
         Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass,
         Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.GrassRight, Tiles.Hay],
        #
        [Tiles.Hay, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtRightCorner, Tiles.Hay]

    ]

    entityData = [PlayerData(Vec2(3, 8)),
                  CoinData(Vec2(5.25, 3.25), 1), SpawnerData(Vec2(10, 3), 5, EnemyType.Pig), SpawnerData(Vec2(6, 3), 5, EnemyType.Cow)]

    m = Map(list(reversed(tiles)), entityData)

    m.save(name)
