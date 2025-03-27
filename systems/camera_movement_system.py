import pygame
import random
from ecs_pattern import System, EntityManager

from entities.player_entity import PlayerEntity
from map import MapResource
from resources import CameraResource
from systems.parallax_system import ParallaxItem, ParallaxLayer, Range, ParallaxManager


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

        # Parallax Layers
        self.ParallaxManager = ParallaxManager(self.screen)

        # Hintergrundbild
        self.BackgroundLayer = ParallaxItem(
            x=0, y=0,
            z_index=0,
            image=pygame.image.load("rsc/img/background/background.png").convert_alpha(),
            scale=(self.screen_width, self.screen_height)
        )
        self.ParallaxManager.add_object(self.BackgroundLayer)
        # Wolken
        self.CloudsLayer = ParallaxLayer(
            image_path="rsc/img/background/clouds.png",
            z_index=1,
            scale=Range(1.8, 2.0)
        )
        self.ParallaxManager.add_object(self.CloudsLayer)
        # Bäume
        self.TreeLayer = ParallaxLayer(
            image_path="rsc/img/background/trees.png",
            z_index=2,
            scale=Range(1.95,2.05)
        )
        self.ParallaxManager.add_object(self.TreeLayer)
        # Büsche
        self.BushLayer = ParallaxLayer(
            image_path="rsc/img/background/bushes.png",
            z_index=3,
            scale=Range(1.45, 1.55)
        )
        self.ParallaxManager.add_object(self.BushLayer)

        self.prev_camera_x = None
        self.prev_camera_y = None


    def init_parallax_layers(self):
        # Wolken
        x: int = 0
        while x < self.screen_width * 2:
            scale = self.CloudsLayer.add_item(x)
            x += scale[0] / 2

        # Bäume
        tree_width = self.TreeLayer.image.get_width() * 2.0
        x = 0
        while x < self.screen_width * 3:
            group_size = random.choice([1, 2]) if random.random() < 0.85 else 1
            for i in range(group_size):
                y_offset = random.randint(360, 370) # Bodennahe Y-Position
                self.TreeLayer.add_item(x + i * tree_width * 0.9, y_offset)
            x += tree_width * group_size + random.randint(100, 300)

        # Büsche
        bush_width = self.BushLayer.image.get_width() * 1.5
        x = 0
        while x < self.screen_width * 3:
            if random.random() < 0.6:
                y_offset = random.randint(395, 410)  # Bodennahe Y-Position
                self.BushLayer.add_item(x, y_offset)
            x += bush_width + random.randint(100, 300)


    def start(self):
        self.camera = next(self.entities.get_by_class(CameraResource))
        self.player_entity = next(self.entities.get_by_class(PlayerEntity))

        self.screen_width_factor: float = self.screen_width / self.camera.screenWidthInTiles
        self.screen_height_factor: float = self.screen_height / self.camera.screenHeightInTiles

        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))

        # Set camera boundaries based on map size
        self.min_camera_x, self.max_camera_x = 0.0, map_rsc.map.width - self.camera.screenWidthInTiles
        self.min_camera_y, self.max_camera_y = 0.0, map_rsc.map.height - self.camera.screenHeightInTiles

        self.init_parallax_layers()

        self.prev_camera_x = self.camera.x
        self.prev_camera_y = self.camera.y

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

        # Parallax Layer zeichnen
        self.ParallaxManager.update(self.camera.x - self.prev_camera_x, self.camera.y - self.prev_camera_y)

        # Kamera-Movement speichern
        self.prev_camera_x = self.camera.x
        self.prev_camera_y = self.camera.y

        # Debug
        #pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)


    def update_parallax_layers_OLD(self):
        dx = self.camera.x - self.prev_camera_x
        dy = self.camera.y - self.prev_camera_y

        # Offset aktualisieren
        self.parallax_offsets["clouds"][0] -= dx * self.screen_width_factor * 0.1
        self.parallax_offsets["clouds"][1] -= dy * self.screen_height_factor * 0.1
        self.parallax_offsets["trees"][0] -= dx * self.screen_width_factor * 0.3
        self.parallax_offsets["trees"][1] -= dy * self.screen_height_factor * 0.01
        self.parallax_offsets["bushes"][0] -= dx * self.screen_width_factor * 0.5
        self.parallax_offsets["bushes"][1] -= dy * self.screen_height_factor * 0.02

        # Wolken zeichnen
        new_clouds = []
        for cloud in self.clouds:
            scale = cloud["scale"]
            img = pygame.transform.smoothscale(
                self.clouds_img,
                (int(self.clouds_img.get_width() * scale), int(self.clouds_img.get_height() * scale))
            )
            x = cloud["x"] + self.parallax_offsets["clouds"][0]
            y = 50 + self.parallax_offsets["clouds"][1] * 0.1
            self.screen.blit(img, (x, y))
            if x + img.get_width() > 0:
                new_clouds.append({"x": cloud["x"], "scale": scale})

        self.clouds = new_clouds

        # Bäume zeichnen (zuerst)
        trees_scaled = pygame.transform.smoothscale(
            self.trees_img,
            (int(self.trees_img.get_width() * 2.0), int(self.trees_img.get_height() * 2.0))
        )
        for tree in self.trees:
            x = tree["x"] + self.parallax_offsets["trees"][0]
            y = tree["y"] + self.parallax_offsets["trees"][1]
            self.screen.blit(trees_scaled, (x, y))

        # Büsche zeichnen (danach, über Bäume)
        bushes_scaled = pygame.transform.smoothscale(
            self.bushes_img,
            (int(self.bushes_img.get_width() * 1.5), int(self.bushes_img.get_height() * 1.5))
        )
        for bush in self.bushes:
            x = bush["x"] + self.parallax_offsets["bushes"][0]
            y = bush["y"] + self.parallax_offsets["bushes"][1]
            self.screen.blit(bushes_scaled, (x, y))