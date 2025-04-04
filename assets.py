from pathlib import Path

import pygame

instance = None


class Assets:

    def __load_all_assets(self):
        self.playerImgs_right = [self.__load_img(f"rsc/img/entities/rooster/rooster{i}.png") for i in range(2)]
        self.playerImgs_left = [pygame.transform.flip(image, True, False) for image in self.playerImgs_right]
        self.playerImgs_invincible_right = [self.__load_img(f"rsc/img/entities/rooster/rooster-invincible{i}.png") for i
                                            in
                                            range(4)]
        self.playerImgs_invincible_left = [pygame.transform.flip(image, True, False) for image in
                                           self.playerImgs_invincible_right]

        self.smokeImgs = [self.__load_img(f"rsc/img/entities/smoke/smoke{i}.png") for i
                          in
                          range(46)]

        self.spawnerImg = {"Pig": self.__load_img("rsc/img/objects/spawner/spawner-pig-16x16.png"),
                           "Cow": self.__load_img("rsc/img/objects/spawner/spawner-cow-16x16.png"),
                           "Sheep": self.__load_img("rsc/img/objects/spawner/spawner-sheep-16x16.png")}

        self.enemyImg_cow = self.__load_img("rsc/img/entities/cow/cow-16x16.png")
        self.enemyImgs_cow_left = [self.__load_img(f"rsc/img/entities/cow/cow_animated{i + 1}-16x16.png") for i in
                                   range(2)]
        self.enemyImgs_cow_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_cow_left]

        self.enemyImg_sheep = self.__load_img("rsc/img/entities/sheep/sheep-16x16.png")
        self.enemyImgs_sheep_left = [self.__load_img(f"rsc/img/entities/sheep/sheep_animated{i + 1}-16x16.png") for i in
                                     range(3)]
        self.enemyImgs_sheep_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_sheep_left]

        self.enemyImg_pig = self.__load_img("rsc/img/entities/pig/pig-16x16.png")
        self.enemyImgs_pig_left = [self.__load_img(f"rsc/img/entities/pig/pig_animated{i + 1}-16x16.png") for i in
                                   range(2)]
        self.enemyImgs_pig_right = [pygame.transform.flip(image, True, False) for image in self.enemyImgs_pig_left]

        self.roosterImg = self.__load_img("rsc/img/entities/rooster/rooster-16x16.png")
        self.roosterImgs_jump = [self.__load_img(f"rsc/img/entities/rooster/rooster_jump{i + 1}-16x16.png") for i in
                                 range(2)]

        self.bunnyImg = self.__load_img("rsc/img/entities/bunny/bunny-16x16.png")

        self.coinImgs = [self.__load_img(f"rsc/img/objects/coin/coin_animated{i + 1}-16x16.png") for i in range(4)]
        self.shitImgs = [self.__load_img(f"rsc/img/objects/shit/shit_animated{i + 1}-16x16.png") for i in range(4)]
        self.eggImgs = [self.__load_img(f"rsc/img/objects/egg/egg_animated{i + 1}-16x16.png") for i in range(4)]
        self.eggDestroyImgs = [self.__load_img(f"rsc/img/objects/egg/egg_animated_destroy{i + 1}-16x16.png") for i in range(6)]
        self.mushroomImgs = [self.__load_img(f"rsc/img/objects/mushroom/mushroom_animated{i + 1}-16x16.png") for i in range(2)]
        self.melonImg = [self.__load_img(f"rsc/img/objects/melon/melon_animated{i + 1}-16x16.png") for i in range(2)]
        self.collectibleImgsDict = {"Coin": self.coinImgs,
                                    "Shit": self.shitImgs,
                                    "Egg": self.eggImgs,
                                    "Mushroom": self.mushroomImgs,
                                    "Melon": self.melonImg}

        self.backgroundMusic = self.__load_audio('rsc/sounds/cyber-farm-271090.mp3', 0.2)
        self.coinCollection = self.__load_audio('rsc/sounds/coin-collection-6075.mp3', 0.9)
        self.shitCollection = self.__load_audio('rsc/sounds/shit-step.mp3', 0.9)
        self.melonCollection = self.__load_audio('rsc/sounds/eat-sound.mp3', 0.9)
        self.eggCollection = self.__load_audio('rsc/sounds/level-win-6416.mp3', 1.0)
        self.player_hit = self.__load_audio('rsc/sounds/retro-hurt-2-236675.mp3', 0.8)

        self.enemyImgsDict = {"Cow": [self.enemyImgs_cow_left, self.enemyImgs_cow_right],
                              "Pig": [self.enemyImgs_pig_left, self.enemyImgs_pig_right],
                              "Sheep": [self.enemyImgs_sheep_left, self.enemyImgs_sheep_right]}

        self.tileImgs = {}
        for file in [file for file in Path("rsc/img/tiles").iterdir() if file.name.endswith("-16x16.png")]:
            self.tileImgs[file.stem.replace("-16x16", "")] = pygame.image.load(file.absolute()).convert_alpha()

    @staticmethod
    def __load_audio(path: str, volume: float):
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
