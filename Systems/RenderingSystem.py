import pygame.transform
from ecs_pattern import System, EntityManager
from pygame import Surface

from Components import SpriteComponent, TransformComponent
from Resources import CameraResource


class RenderingSystem(System):
    def __init__(self, entities: EntityManager, screen: Surface):
        self.entities = entities
        self.screen = screen

    def update(self):
        for entity in self.entities.get_with_component(SpriteComponent, TransformComponent):
            sprite: SpriteComponent = entity
            transform: TransformComponent = entity

            screenWidth, screenHeight = pygame.display.get_surface().get_size()
            camera: CameraResource = next(self.entities.get_by_class(CameraResource))

            tileWidthInPixel, tileHeightInPixel = screenWidth / camera.screenWidthInTiles, screenHeight / camera.screenHeightInTiles

            p = pygame.transform.scale(sprite.sprite, (
                int(tileWidthInPixel * transform.width), int(tileHeightInPixel * transform.height)))
            self.screen.blit(p, (
                int((transform.position.x - camera.x) * tileWidthInPixel),
                int(screenHeight - (
                        transform.position.y - camera.y) * tileHeightInPixel - transform.height * tileHeightInPixel)))
