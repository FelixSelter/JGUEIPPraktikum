from pathlib import Path

import pygame

instance = None


class Assets:

    def __load_all_assets(self):
        self.playerImgs = [self.__load_img(f"rsc/img/example{i}.bmp") for i in range(3)]

        self.enemyImg_cow = self.__load_img("rsc/img/entities/cow.bmp")
        self.enemyImg_pig = self.__load_img("rsc/img/entities/pig.bmp")
        self.enemyImg_sheep = self.__load_img("rsc/img/entities/sheep.bmp")

        self.coinImg = self.__load_img("rsc/img/objects/coin.bmp")

        self.backgroundMusic = self.__load_audio('rsc/sounds/cyber-farm-271090.mp3', 0.5)

        self.tileImgs = {}
        for file in [file for file in Path("rsc/img/tiles").iterdir() if file.suffix == ".bmp"]:
            self.tileImgs[file.stem] = pygame.image.load(file.absolute()).convert_alpha()

    @staticmethod
    def __load_audio(path, volume):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound

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
