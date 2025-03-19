from Map import Tiles, Map

if __name__ == "__main__":
    m = Map([
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Dirt, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Air,
         Tiles.Air, Tiles.Air, Tiles.Air, Tiles.Hay],
        [Tiles.Hay, Tiles.GrassLeft, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass,
         Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass,
         Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.Grass, Tiles.GrassRight, Tiles.Hay],
        [Tiles.Hay, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom,
         Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtBottom, Tiles.DirtRightCorner, Tiles.Hay]

    ])
    m.save("Level1")
