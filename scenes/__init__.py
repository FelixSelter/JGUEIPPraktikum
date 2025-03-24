from abc import abstractmethod

import pygame_gui
from ecs_pattern import EntityManager
from pygame import Surface


class Scene:
    entities = EntityManager()
    system_manager: None

    def __init__(self, screen: Surface, theme: str):
        self.ui_manager = pygame_gui.UIManager((screen.width, screen.height), theme)

    @abstractmethod
    def load(self):
        pass

    def destroy(self):
        self.entities._entity_map = {}

    def start(self):
        self.system_manager.start_systems()

    def stop(self):
        self.system_manager.stop_systems()

    def update(self):
        self.system_manager.update_systems()
