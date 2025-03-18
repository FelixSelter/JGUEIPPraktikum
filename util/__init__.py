from pathlib import Path

import pygame

instance = None


class Assets:

    def __init__(self):
        global instance
        instance = self

        self.player = pygame.image.load("rsc/example.bmp").convert_alpha()
        self.coin = pygame.image.load("rsc/coin.bmp").convert_alpha()

        self.tiles = {}
        for file in Path("rsc/Tiles").iterdir():
            self.tiles[file.name] = pygame.image.load(file.absolute()).convert_alpha()

    @staticmethod
    def get():
        if instance is None:
            return Assets()
        return instance
