import os

import pygame

from assets import Assets
from scenes.game_scene import GameScene
from scenes.leveleditor_scene import LevelEditorScene

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Mittiges Fenster


def App():
    pygame.init()
    pygame.display.set_caption("Super Chicken 16")

    screen = pygame.display.set_mode((16 * 80, 9 * 80))
    clock = pygame.time.Clock()

    scene = GameScene(screen, "rsc/Maps/14.map")
    #scene = LevelEditorScene(screen, "rsc/Maps/87.map")

    scene.load()
    scene.start()

    while True:
        screen.fill((0, 0, 0))
        clock.tick_busy_loop(60)
        scene.update()
        pygame.display.flip()


if __name__ == '__main__':
    App()
