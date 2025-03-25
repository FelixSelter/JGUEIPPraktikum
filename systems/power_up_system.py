from ecs_pattern import System, EntityManager

from components.player_component import PlayerComponent
from components.power_up_component import PowerUpComponent
from entities.enemy_entity import EnemyData
from entities.player_entity import PlayerEntity
from entities.power_up_entity import PowerUpEntity
from resources import TimeResource
from util.additional_math import Vec2

import random

class PowerUpSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for player in self.entities.get_with_component(PlayerComponent):
            player: PlayerEntity = player
            for powerUp in player.statusEffects:
                powerUp[0] -= time_rsc.deltaTime
                if powerUp[0] <= 0:
                    player.jump -= powerUp[1]
                    del player.statusEffects[0]
