from abc import abstractmethod

from ecs_pattern import EntityManager


class Scene:
    entities = EntityManager()
    system_manager: None

    @abstractmethod
    def create(self):
        pass

    def destroy(self):
        self.entities._entity_map = {}

    def start(self):
        self.system_manager.start_systems()

    def stop(self):
        self.system_manager.stop_systems()

    def update(self):
        self.system_manager.update_systems()
