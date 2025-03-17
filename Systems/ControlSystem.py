import pygame
from ecs_pattern import System, EntityManager
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_a, K_d, K_SPACE

from Resources import GlobalStateResource
from Entities import PlayerEntity


class ControllerSystem(System):
    def __init__(self, entities: EntityManager, event_getter):
        self.entities = entities
        self.event_getter = event_getter
        self.game_state_info = None
        self.player_entity = None

    def start(self):
        self.game_state_info = next(self.entities.get_by_class(GlobalStateResource))
        self.player_entity = next(self.entities.get_by_class(PlayerEntity))

    def update(self):
        for event in self.event_getter():
            event_type = event.type
            event_key = getattr(event, 'key', None)

            # Quit game
            if event_type == QUIT:
                self.game_state_info.play = False

            # Pause game
            if event_key == K_ESCAPE:
                self.game_state_info.pause = not self.game_state_info.pause

            # Movement
            if event_key == K_a:  # Links
                # Start
                if event_type == KEYDOWN:
                    self.player_entity.speed.x -= 2
                # End
                else:
                    self.player_entity.speed.x = 0

            if event_key == K_d:  # Rechts
                # Start
                if event_type == KEYDOWN:
                    self.player_entity.speed.x += 2
                # End
                else:
                    self.player_entity.speed.x = 0

            if event_key == K_SPACE:  # Sprung
                # Start
                if event_type == KEYDOWN:
                    self.player_entity.speed.y = 2
                # End
                else:
                    self.player_entity.speed.y = 0
