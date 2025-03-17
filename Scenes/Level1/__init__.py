from ecs_pattern import System, EntityManager


class Level1InitSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def start(self):
        pass

    def stop(self):
        pass
