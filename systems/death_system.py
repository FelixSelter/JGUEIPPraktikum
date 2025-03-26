from ecs_pattern import System, EntityManager

from components.health_component import HealthComponent
from entities.player_entity import PlayerEntity
from events import EventManagerResource
from events.game_end_event import GameEndEventName, GameEndEvent, GameEndEventType


class PurgeDeleteBufferSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        for entity in self.entities.get_with_component(HealthComponent):
            if entity.health <= 0:
                if isinstance(entity, PlayerEntity):
                    next(self.entities.get_by_class(EventManagerResource)).emit_event(GameEndEventName.GameLost,
                                                                                      GameEndEvent(
                                                                                          GameEndEventType.GameLost))
                else:
                    self.entities.delete_buffer_add(entity)

        self.entities.delete_buffer_purge()
