import pygame


class App():
    new_scene = None
    scene = None

    def change_scene(self, scene):
        self.new_scene = scene

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Super Chicken 16")

        self.screen = pygame.display.set_mode((16 * 80, 9 * 80))
        self.clock = pygame.time.Clock()

    def update(self):
        if self.new_scene is not None:
            if self.scene is not None:
                self.scene.stop()
                self.scene.destroy()
            self.scene, self.new_scene = self.new_scene, None
            self.scene.load()
            self.scene.start()

        if self.scene is not None:
            self.scene.update()


app = App()
