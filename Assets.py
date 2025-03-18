from pathlib import Path

import pygame

instance = None


class Assets:

    def __load_all_assets(self):
        self.playerImg = self.__load_img("rsc/img/example.bmp")
        self.coinImg = self.__load_img("rsc/img/objects/coin.bmp")

        self.tileImgs = {}
        for file in [file for file in Path("rsc/img/tiles").iterdir() if file.suffix == ".bmp"]:
            self.tileImgs[file.stem] = pygame.image.load(file.absolute()).convert_alpha()

    @staticmethod
    def __load_img(path):
        return pygame.image.load(path).convert_alpha()

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
