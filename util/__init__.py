from pathlib import Path

import pygame

instance = None


class Assets:

    def __load_all_assets(self):
        self.playerImg = pygame.image.load("rsc/example.bmp").convert_alpha()
        self.coinImg = pygame.image.load("rsc/coin.bmp").convert_alpha()

        self.tileImgs = {}
        for file in Path("rsc/Tiles").iterdir():
            self.tileImgs[file.stem] = pygame.image.load(file.absolute()).convert_alpha()

    @staticmethod
    def get():
        if instance is None:
            return Assets()
        return instance

    def __init__(self):
        global instance
        if instance is not None:
            raise Exception("Tried to create multiple instances of the Asset manager")
        instance = self
        self.__load_all_assets()
