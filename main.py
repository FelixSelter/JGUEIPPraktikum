import os

import pygame
from ecs_pattern import EntityManager, SystemManager

from Resources import GlobalStateResource
from Systems.CollisionSystem import CollisionSystem
from Systems.GravitySystem import GravitySystem
from Systems.InitSystem import InitSystem
from Systems.MovementSystem import MovementSystem
from Systems.RenderingSystem import RenderingSystem
from Systems.ControlSystem import ControllerSystem
from Systems.TileCollisionSystem import TileCollisionSystem
from Systems.TimeSystem import TimeSystem

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Mittiges Fenster


def App():
    pygame.init()
    pygame.display.set_caption("Super Chicken 16")

    screen = pygame.display.set_mode((16 * 100, 9 * 100))
    clock = pygame.time.Clock()

    entities = EntityManager()

    system_manager = SystemManager([
        InitSystem(entities),
        TimeSystem(entities),
        ControllerSystem(entities, pygame.event.get),
        GravitySystem(entities),
        MovementSystem(entities),
        TileCollisionSystem(entities),
        CollisionSystem(entities),
        RenderingSystem(entities, screen)
    ])

    system_manager.start_systems()

    global_state: GlobalStateResource = next(entities.get_by_class(GlobalStateResource))
    while global_state.play:
        screen.fill((0, 0, 0))

        clock.tick_busy_loop(60)
        system_manager.update_systems()

        pygame.display.flip()

    system_manager.stop_systems()


if __name__ == '__main__':
    App()
