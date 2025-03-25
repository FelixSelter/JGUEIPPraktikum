import os

import pygame

from app import app
from assets import Assets
from scenes.mainmenu_scene import MainMenuScene

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Mittiges Fenster

if __name__ == '__main__':
    pygame.mixer.Sound.play(Assets.get().backgroundMusic)
    app.change_scene(MainMenuScene(app.screen))

    while True:
        app.screen.fill((0, 0, 0))
        app.clock.tick_busy_loop(60)
        app.update()
        pygame.display.flip()
