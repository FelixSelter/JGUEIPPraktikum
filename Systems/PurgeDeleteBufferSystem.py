from ecs_pattern import System, EntityManager


class PurgeDeleteBufferSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        self.entities.delete_buffer_purge()
