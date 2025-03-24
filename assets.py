from pathlib import Path

import pygame

instance = None


class Assets:

    def __load_all_assets(self):
        #self.playerImgs = [self.__load_img(f"rsc/img/example{i}.bmp") for i in range(3)]
        self.playerImgs = [self.__load_img(f"rsc/img/entities/rooster/rooster{i}.png") for i in range(2)]

        self.enemyImg_cow = self.__load_img("rsc/img/entities/cow/cow.bmp")
        self.enemyImgs_cow_left = [self.__load_img(f"rsc/img/entities/cow/cow_animated{i + 1}.bmp") for i in range(2)]
        self.enemyImgs_cow_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_cow_left]

        self.enemyImg_sheep = self.__load_img("rsc/img/entities/sheep/sheep.bmp")
        self.enemyImgs_sheep_left = [self.__load_img(f"rsc/img/entities/sheep/sheep_animated{i + 1}.bmp") for i in
                                     range(3)]
        self.enemyImgs_sheep_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_sheep_left]

        self.enemyImg_pig = self.__load_img("rsc/img/entities/pig/pig.bmp")
        self.enemyImgs_pig_left = [self.__load_img(f"rsc/img/entities/pig/pig_animated{i + 1}.bmp") for i in range(2)]
        self.enemyImgs_pig_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_pig_left]

        self.roosterImg = self.__load_img("rsc/img/entities/rooster/rooster.bmp")
        self.roosterImgs_jump = [self.__load_img(f"rsc/img/entities/rooster/rooster_jump{i + 1}.bmp") for i in range(2)]

        self.coinImgs = [self.__load_img(f"rsc/img/objects/coin/coin_animated{i + 1}.bmp") for i in range(4)]
        self.shitImgs = [self.__load_img(f"rsc/img/objects/shit/shit_animated{i + 1}.bmp") for i in range(4)]
        self.eggImgs = [self.__load_img(f"rsc/img/objects/egg/egg_animated{i + 1}.bmp") for i in range(4)]
        self.mushroomImgs = [self.__load_img(f"rsc/img/objects/mushroom/mushroom_animated{i + 1}.bmp") for i in
                             range(2)]
        self.collectibleImgsDict = {"Coin": self.coinImgs,
                              "Shit": self.shitImgs,
                              "Egg": self.eggImgs,
                              "Mushroom": self.mushroomImgs}


        self.backgroundMusic = self.__load_audio('rsc/sounds/cyber-farm-271090.mp3', 0.5)

        self.enemyImgsDict = {"Cow": [self.enemyImgs_cow_left, self.enemyImgs_cow_right],
                              "Pig": [self.enemyImgs_pig_left, self.enemyImgs_pig_right],
                              "Sheep": [self.enemyImgs_sheep_left, self.enemyImgs_sheep_right]}

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
