import sys
from enum import Enum
from math import floor, ceil, sqrt, inf, copysign
from typing import Any, List

import pygame
from pygame import Surface, QUIT, K_ESCAPE

from components.movement_component import MovementComponent
from components.transform_component import TransformComponent
from entities.player_entity import PlayerData
from map import MapResource, Map
from util.additional_math import sign_zero, Vec2, fract

epsilon = 0.0001


class CollisionDirection(Enum):
    Top = 0
    Bottom = 1
    Right = 2
    Left = 3


def x_to_px(x):
    return x * 80


def y_to_px(y):
    return 9 * 80 - y * 80


def moveUntilCollision(entity: Any, targetDeltaX: float, targetDeltaY: float, map: MapResource, screen: Surface):
    print("\n\n")
    if targetDeltaX == 0 and targetDeltaY == 0:
        return

    transform: TransformComponent = entity
    movement: MovementComponent = entity

    for cell_x in range(16):
        for cell_y in range(9):
            if map.map.tiles[cell_y][cell_x].isSolid():
                pygame.draw.rect(screen, (100, 100, 100), (x_to_px(cell_x), y_to_px(cell_y) - 80, 80, 80))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x_to_px(cell_x), y_to_px(cell_y) - 80, 80, 80), 2)

    # Direction of movement
    horizontal_direction = sign_zero(targetDeltaX)
    vertical_direction = sign_zero(targetDeltaY)

    pygame.draw.rect(screen, (255, 0, 0), (x_to_px(transform.position.x), y_to_px(transform.position.y) - 80, 80, 80),
                     2)
    pygame.draw.circle(screen, (0, 255, 0),
                       (x_to_px(transform.position.x + (0 if horizontal_direction < 0 else 1) + targetDeltaX),
                        y_to_px(transform.position.y + (0 if vertical_direction < 0 else 1) + targetDeltaY)),
                       8)
    pygame.draw.line(screen, (0, 0, 0), (
        x_to_px(transform.position.x + (0 if horizontal_direction < 0 else 1)),
        y_to_px(transform.position.y + (0 if vertical_direction < 0 else 1))),
                     (x_to_px(transform.position.x + targetDeltaX + (0 if horizontal_direction < 0 else 1)),
                      y_to_px(transform.position.y + (0 if vertical_direction < 0 else 1) + targetDeltaY)),
                     3)

    # How much distance needs to be traveled from each hitbox edge to reach the next tile edge
    initial_distance_left = -fract(transform.position.x)
    initial_distance_down = -fract(transform.position.y)
    initial_distance_right = ceil(transform.position.x + transform.width) - (transform.position.x + transform.width)
    initial_distance_up = ceil(transform.position.y + transform.height) - (transform.position.y + transform.height)

    # Initialise them with the distance required to align to the grid
    # After the first step they will be 1 as we either move
    step_x = initial_distance_left if horizontal_direction < 0 else initial_distance_right
    step_y = initial_distance_down if vertical_direction < 0 else initial_distance_up

    # How much x/y change if the entity moves one cell vertical/horizontal
    y_increment_for_one_x_step = copysign(targetDeltaY / targetDeltaX if not targetDeltaX == 0 else inf,
                                          vertical_direction)
    x_increment_for_one_y_step = copysign(targetDeltaX / targetDeltaY if not targetDeltaY == 0 else inf,
                                          horizontal_direction)

    # The algorithm decides to move horizontal/vertical depending on what distance to the next tile edge is shorter
    # If we move in x/y direction that decreases the distance to the next vertical/horizontal edge
    current_distance_x = sqrt(step_x ** 2 + (y_increment_for_one_x_step * abs(step_x)) ** 2)
    current_distance_y = sqrt(step_y ** 2 + (x_increment_for_one_y_step * abs(step_y)) ** 2)

    # We need these to reset current_distance_x, current_distance_y if we aligned with a tile edge
    distance_moved_for_one_x_step = sqrt(1 + y_increment_for_one_x_step ** 2)
    distance_moved_for_one_y_step = sqrt(x_increment_for_one_y_step ** 2 + 1)

    # The current position relative to the entity position
    # If we move right/up we start at the right/top edge and align that to the grid
    edge_offset_x = 0 if horizontal_direction < 0 else transform.width
    edge_offset_y = 0 if vertical_direction < 0 else transform.height

    # Where we want to move relative to the current position
    # Position is relative to the bottom left hitbox corner
    # If our calculation is relative to the right/top edge we need to travel this distance additionally
    target_x = targetDeltaX + (0 if horizontal_direction < 0 else transform.width)
    target_y = targetDeltaY + (0 if vertical_direction < 0 else transform.height)

    collision_direction = None

    while True:
        print()

        # Check if target can be reached
        if abs(target_x - edge_offset_x) < abs(step_x) and abs(target_y - edge_offset_y) < abs(step_y):
            break

        # Move one step horizontal
        elif current_distance_x < current_distance_y:
            collision_direction = CollisionDirection.Right if horizontal_direction < 0 else CollisionDirection.Left
            edge_offset_x += step_x  # Move one step horizontally
            y_move_amount = y_increment_for_one_x_step * abs(step_x)
            edge_offset_y += y_move_amount  # Move y accordingly
            current_distance_y -= distance_moved_for_one_x_step * abs(
                step_x)  # Moving horizontal decreases distance to the next horizontal edge
            current_distance_x = distance_moved_for_one_x_step  # We are aligned with an edge. Reaching the next edge requires a step of 1
            step_x = horizontal_direction  # Once aligned we move in steps of one
            step_y -= y_move_amount

            # Move one step vertical
        else:
            collision_direction = CollisionDirection.Top if vertical_direction < 0 else CollisionDirection.Bottom
            edge_offset_y += step_y  # Move one step vertically
            x_move_amount = x_increment_for_one_y_step * abs(step_y)  # Move x accordingly
            edge_offset_x += x_move_amount
            current_distance_x -= distance_moved_for_one_y_step * abs(
                step_y)  # Moving vertical decreases distance to the next horizontal edge
            current_distance_y = distance_moved_for_one_y_step  # We are aligned with an edge. Reaching the next edge requires a step of 1
            step_y = vertical_direction  # Once aligned we move in steps of one
            step_x -= x_move_amount

        pygame.draw.circle(screen, (0, 0, 255),
                           (x_to_px(transform.position.x + edge_offset_x),
                            y_to_px(transform.position.y + edge_offset_y)),
                           8)

        # Make offsets relative to the player position again
        pos_offset_x, pos_offset_y = edge_offset_x, edge_offset_y
        if not horizontal_direction < 0:
            pos_offset_x -= transform.width
        if not vertical_direction < 0:
            pos_offset_y -= transform.height

        # Collision detection
        collision_tiles: List[(int, int)] = []
        match collision_direction:
            case CollisionDirection.Left:
                # Check all tiles right of the player
                for cell_y in range(floor(transform.position.y + pos_offset_y),
                                    floor(transform.position.y + pos_offset_y + transform.height + epsilon) + 1):
                    collision_tiles.append(
                        (floor(transform.position.x + transform.width + pos_offset_x + epsilon), cell_y))

            case CollisionDirection.Right:
                # Check all tiles left of the player
                for cell_y in range(floor(transform.position.y + pos_offset_y),
                                    floor(transform.position.y + pos_offset_y + epsilon) + 2):
                    collision_tiles.append((floor(transform.position.x + pos_offset_x) - 1, cell_y))

            case CollisionDirection.Top:
                # Check all tiles below the player
                for cell_x in range(floor(transform.position.x + pos_offset_x),
                                    floor(transform.position.x + pos_offset_x + transform.width + epsilon) + 1):
                    collision_tiles.append((cell_x, floor(transform.position.y + pos_offset_y) - 1))

            case CollisionDirection.Bottom:
                # Check all tiles above the player
                for cell_x in range(floor(transform.position.x + pos_offset_x),
                                    floor(transform.position.x + pos_offset_x + transform.width + epsilon) + 1):
                    collision_tiles.append((cell_x, floor(transform.position.y + pos_offset_y) + 1))

        collided = False
        for cell_x, cell_y in collision_tiles:
            if not (0 <= cell_x < map.map.width and 0 <= cell_y < map.map.height):
                continue

            pygame.draw.circle(screen, (255, 0, 255),
                               (x_to_px(cell_x + 0.5),
                                y_to_px(cell_y + 0.5)),
                               8)

            if map.map.tiles[cell_y][cell_x].isSolid():
                pygame.draw.circle(screen, (255, 0, 255),
                                   (x_to_px(cell_x + 0.5),
                                    y_to_px(cell_y + 0.5)),
                                   8)

                # Call the collision handler

                pygame.draw.rect(screen, (0, 255, 0),
                                 (x_to_px(transform.position.x + pos_offset_x),
                                  y_to_px(transform.position.y + pos_offset_y) - 80, 80, 80),
                                 2)

                if collision_direction in [CollisionDirection.Right, CollisionDirection.Left]:
                    movement.speed.x = 0
                    movement.acceleration.x = 0
                else:
                    movement.speed.y = 0
                    movement.acceleration.y = 0

                collided = True
                break

        if collided:
            break


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Super Chicken 16")

    screen = pygame.display.set_mode((16 * 80, 9 * 80))
    clock = pygame.time.Clock()

    entity = PlayerData(Vec2(5.1, 2.3)).deserialize()
    m = Map.load("rsc/Maps/Level1")

    while True:
        screen.fill((255, 255, 255))
        clock.tick_busy_loop(10)

        for event in pygame.event.get():
            event_type = event.type
            event_key = getattr(event, 'key', None)

            # Quit game
            if event_type == QUIT or event_key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        moveUntilCollision(entity, pygame.mouse.get_pos()[0] / 80 - entity.position.x,
                           8 - pygame.mouse.get_pos()[1] / 80 - entity.position.y,
                           MapResource(
                               map=m
                           ), screen)

        pygame.display.flip()
