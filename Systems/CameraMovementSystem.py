import pygame
from ecs_pattern import System, EntityManager
from Resources import CameraResource
from Entities import PlayerEntity



class CameraMovementSystem(System):
    def __init__(self, entity_manager: EntityManager, screen: pygame.Surface):
        self.entities = entity_manager
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.camera: CameraResource = None
        self.player_entity: PlayerEntity = None

        # Mittiges Rechteck
        rect_width = self.screen_width // 2.8
        rect_height = self.screen_height // 1.9
        self.rect = pygame.Rect(
            (self.screen_width - rect_width) // 2,
            (self.screen_height - rect_height) // 2,
            rect_width, rect_height
        )


    def start(self):
        self.camera = next(self.entities.get_by_class(CameraResource))
        self.player_entity = next(self.entities.get_by_class(PlayerEntity))


    def update(self):
        player_x: float = self.player_entity.position.x
        player_y: float = self.player_entity.position.y

        # Bildschirm Koordinaten
        screen_xl = (player_x - self.camera.x) * (self.screen_width / self.camera.screenWidthInTiles)
        screen_xr = (player_x - self.camera.x + self.player_entity.width) * (self.screen_width / self.camera.screenWidthInTiles)
        screen_yb = (player_y - self.camera.y) * (self.screen_height / self.camera.screenHeightInTiles)
        screen_yt = (player_y - self.camera.y + self.player_entity.height) * (self.screen_height / self.camera.screenHeightInTiles)

        # Horizontales Verlassen
        if screen_xl < self.rect.x:
            self.camera.x -= (self.rect.x - screen_xl) / (self.screen_width / self.camera.screenWidthInTiles)
        elif screen_xr > self.rect.right:
            self.camera.x += ((screen_xr + self.player_entity.width) - self.rect.right) / (
                        self.screen_width / self.camera.screenWidthInTiles)

        # Vertikales Verlassen
        if screen_yb < self.rect.y:
            self.camera.y -= (self.rect.y - screen_yb) / (self.screen_height / self.camera.screenHeightInTiles)
        elif screen_yt > self.rect.bottom:
            self.camera.y += (screen_yt - self.rect.bottom) / (
                        self.screen_height / self.camera.screenHeightInTiles)


        # Debug
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
