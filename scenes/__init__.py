from abc import abstractmethod
from typing import Callable, Optional

import pygame_gui
from ecs_pattern import EntityManager, SystemManager
from pygame import Surface


class Scene:
    entities = EntityManager()
    system_manager: SystemManager = None

    def __init__(self, screen: Surface, theme: Optional[str] = None, preload_fonts: Optional[Callable[[pygame_gui.UIManager], None]] = None):
        self.ui_manager = pygame_gui.UIManager((screen.width, screen.height))

        if preload_fonts: preload_fonts(self.ui_manager)

        if theme:
            self.ui_manager.get_theme().load_theme(theme)


        self.entities.add_buffer = []

    @abstractmethod
    def load(self):
        pass

    def destroy(self):
        self.ui_manager.clear_and_reset()
        self.entities.delete(*self.entities.get_with_component())

    def start(self):
        self.system_manager.start_systems()

    def stop(self):
        self.system_manager.stop_systems()

    def update(self):
        self.system_manager.update_systems()
