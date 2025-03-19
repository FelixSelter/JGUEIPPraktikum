import pygame
from ecs_pattern import System, EntityManager

from Entities.Player import PlayerEntity
from Map import MapResource
from Resources import CameraResource


class CameraMovementSystem(System):
    def __init__(self, entity_manager: EntityManager, screen: pygame.Surface):
        self.entities: EntityManager = entity_manager
        self.screen: pygame.Surface = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.camera: CameraResource = None
        self.player_entity: PlayerEntity = None
        self.screen_width_factor, self.screen_height_factor = None, None
        self.min_camera_x, self.max_camera_x = None, None
        self.min_camera_y, self.max_camera_y = None, None

        # Mittiges Rechteck
        rect_width: float = self.screen_width // 2.8
        rect_height: float = self.screen_height // 1.9
        self.rect = pygame.Rect(
            (self.screen_width - rect_width) // 2,
            (self.screen_height - rect_height) // 2,
            rect_width, rect_height
        )

    def start(self):
        self.camera = next(self.entities.get_by_class(CameraResource))
        self.player_entity = next(self.entities.get_by_class(PlayerEntity))

        self.screen_width_factor: float = self.screen_width / self.camera.screenWidthInTiles
        self.screen_height_factor: float = self.screen_height / self.camera.screenHeightInTiles

        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))

        # Set camera boundaries based on map size
        self.min_camera_x, self.max_camera_x = 0.0, map_rsc.map.width - self.camera.screenWidthInTiles
        self.min_camera_y, self.max_camera_y = 0.0, map_rsc.map.height - self.camera.screenHeightInTiles

    def update(self):
        player_x: float = self.player_entity.position.x
        player_y: float = self.player_entity.position.y

        # Bildschirm Koordinaten
        screen_xl = (player_x - self.camera.x) * self.screen_width_factor
        screen_xr = (player_x - self.camera.x + self.player_entity.width) * self.screen_width_factor
        screen_yb = (player_y - self.camera.y) * self.screen_height_factor
        screen_yt = (player_y - self.camera.y + self.player_entity.height) * self.screen_height_factor

        # Horizontales Verlassen
        if screen_xl < self.rect.x:
            self.camera.x -= (self.rect.x - screen_xl) / self.screen_width_factor
        elif screen_xr > self.rect.right:
            self.camera.x += ((screen_xr + self.player_entity.width) - self.rect.right) / self.screen_width_factor

        # Vertikales Verlassen
        if screen_yb < self.rect.y:
            self.camera.y -= (self.rect.y - screen_yb) / self.screen_height_factor
        elif screen_yt > self.rect.bottom:
            self.camera.y += (screen_yt - self.rect.bottom) / self.screen_height_factor

        # Kamera innerhalb Ränder (nicht vor/hinter Map schauen)
        self.camera.x = max(self.min_camera_x, min(self.camera.x, self.max_camera_x))
        self.camera.y = max(self.min_camera_y, min(self.camera.y, self.max_camera_y))

        # Debug
        pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)
