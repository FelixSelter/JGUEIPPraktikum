import pygame, sys
from ecs_pattern import System, EntityManager
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_a, K_d, K_SPACE

from Resources import GlobalStateResource, TimeResource
from Entities import PlayerEntity


class ControllerSystem(System):
    def __init__(self, entities: EntityManager, event_getter):
        self.entities = entities
        self.event_getter = event_getter
        self.game_state_info = None
        self.time_rsc = None
        self.player_entity = None

        self.horizontal_start_speed: float = 1
        self.start_vertical_speed = 2
        self.max_acceleration: float = 3
        self.min_speed: float = 0.1

        self.horizontal_speed: float = 0
        self.horizontal_acceleration: float = 0
        self.horizontal_direction: int = 0
        self.max_speed = self.horizontal_start_speed + self.max_acceleration

        self.movement_keys = {K_a: False, K_d: False}


    def calculate_speed(self):
        if self.horizontal_direction == 0:
            # Abbremsen
            brake_factor = max(0.85, 1 - (abs(self.horizontal_speed) / self.max_speed) * 0.5)

            if abs(self.horizontal_speed) < self.min_speed:
                self.horizontal_speed = 0
            else:
                self.horizontal_speed *= brake_factor

        else:
            if self.player_entity.speed.x == 0:
                self.horizontal_speed += self.horizontal_start_speed * self.horizontal_direction

            if abs(self.horizontal_speed) < self.max_speed:

                # Beschleunigen
                dist = (self.max_acceleration - self.horizontal_acceleration)
                dist = (dist > 0.05) and dist or 0.05
                self.horizontal_acceleration = min(self.max_acceleration, abs(self.horizontal_acceleration) + dist / 15) * self.horizontal_direction

            if abs(self.horizontal_speed) < self.max_speed:
                self.horizontal_speed += self.horizontal_acceleration
            else:
                print("Max")

        self.player_entity.speed.x = self.horizontal_speed


    def start(self):
        self.game_state_info = next(self.entities.get_by_class(GlobalStateResource))
        self.time_rsc = next(self.entities.get_by_class(TimeResource))
        self.player_entity = next(self.entities.get_by_class(PlayerEntity))


    def update(self):
        for event in self.event_getter():
            event_type = event.type
            event_key = getattr(event, 'key', None)

            # Quit game
            if event_type == QUIT:
                self.game_state_info.play = False
                sys.exit()

            # Pause game
            if event_key == K_ESCAPE:
                pygame.quit()
                self.game_state_info.play = False
                sys.exit()
                #self.game_state_info.pause = not self.game_state_info.pause

            # Vertical Movement
            if event_key == K_SPACE:  # Sprung
                # Start
                if event_type == KEYDOWN and self.player_entity.speed.y == 0:
                    self.player_entity.speed.y = 1 + self.start_vertical_speed
                # End
                else:
                    self.player_entity.speed.y = 0

            # Horizontal Movement
            if event_key in self.movement_keys:
                # Start
                if event_type == KEYDOWN:
                    self.movement_keys[event_key] = True
                # End
                else:
                    self.movement_keys[event_key] = False

        # Horizontal Movement
        if self.movement_keys[K_a] and not self.movement_keys[K_d]:
            # Links
            self.horizontal_direction = -1
        elif self.movement_keys[K_d] and not self.movement_keys[K_a]:
            # Rechts
            self.horizontal_direction = 1
        else:
            # Beides oder keins
            self.horizontal_direction = 0

        self.calculate_speed()


