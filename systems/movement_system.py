from enum import Enum
from math import copysign, floor, sqrt, inf, ceil
from typing import Any, List

from ecs_pattern import System, EntityManager

from components.movement_component import MovementComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from entities.player_entity import PlayerEntity
from map import MapResource
from resources import TimeResource
from events import EventManagerResource
from events.game_end_event import GameEndEventName, GameEndEvent, GameEndEventType
from util import CollisionDirection
from util.additional_math import sign_zero, fract

epsilon = 0.0001


def moveUntilCollision(entity: Any, target_delta_x: float, target_delta_y: float, map_rsc: MapResource,
                       entities: EntityManager):
    if target_delta_x == 0 and target_delta_y == 0:
        return

    transform: TransformComponent = entity
    movement: MovementComponent = entity
    tile_collider: TileColliderComponent = entity

    # Direction of movement
    horizontal_direction = sign_zero(target_delta_x)
    vertical_direction = sign_zero(target_delta_y)

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
    y_increment_for_one_x_step = copysign(target_delta_y / target_delta_x if not target_delta_x == 0 else inf,
                                          vertical_direction)
    x_increment_for_one_y_step = copysign(target_delta_x / target_delta_y if not target_delta_y == 0 else inf,
                                          horizontal_direction)

    # The algorithm decides to move horizontal/vertical depending on what distance to the next tile edge is shorter
    # If we move in x/y direction that decreases the distance to the next vertical/horizontal edge
    current_distance_x = sqrt(
        step_x ** 2 + (y_increment_for_one_x_step * abs(step_x)) ** 2) if not abs(
        y_increment_for_one_x_step) == inf else inf
    current_distance_y = sqrt(
        step_y ** 2 + (x_increment_for_one_y_step * abs(step_y)) ** 2) if not abs(
        x_increment_for_one_y_step) == inf else inf

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
    target_x = target_delta_x + (0 if horizontal_direction < 0 else transform.width)
    target_y = target_delta_y + (0 if vertical_direction < 0 else transform.height)

    collision_direction = None

    while True:

        # Check if target can be reached
        if abs(target_x - edge_offset_x) <= abs(step_x) and abs(target_y - edge_offset_y) <= abs(step_y):
            transform.position.x += target_delta_x
            transform.position.y += target_delta_y
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
                                    floor(transform.position.y + pos_offset_y + transform.height - epsilon) + 1):
                    collision_tiles.append(
                        (floor(transform.position.x + transform.width + pos_offset_x), cell_y))

            case CollisionDirection.Right:
                # Check all tiles left of the player
                for cell_y in range(floor(transform.position.y + pos_offset_y),
                                    floor(transform.position.y + pos_offset_y + transform.height - epsilon) + 1):
                    collision_tiles.append((floor(transform.position.x + pos_offset_x) - 1, cell_y))

            case CollisionDirection.Top:
                # Check all tiles below the player
                for cell_x in range(floor(transform.position.x + pos_offset_x),
                                    floor(transform.position.x + pos_offset_x + transform.width - epsilon) + 1):
                    collision_tiles.append((cell_x, floor(transform.position.y + pos_offset_y) - 1))

            case CollisionDirection.Bottom:
                # Check all tiles above the player
                for cell_x in range(floor(transform.position.x + pos_offset_x),
                                    floor(transform.position.x + pos_offset_x + transform.width - epsilon) + 1):
                    collision_tiles.append((cell_x, floor(transform.position.y + pos_offset_y) + 1))

        collided = False
        for cell_x, cell_y in collision_tiles:
            if not (0 <= cell_x < map_rsc.map.width and 0 <= cell_y < map_rsc.map.height):
                continue

            if map_rsc.map.tiles[cell_y][cell_x].isSolid():

                # Move until collision
                transform.position.x += pos_offset_x
                transform.position.y += pos_offset_y

                # Cancel all x movement
                if collision_direction in [CollisionDirection.Right, CollisionDirection.Left]:
                    movement.speed.x = 0
                    # Try to continue moving in y direction
                    if not movement.speed.y == 0:
                        moveUntilCollision(entity, 0, target_delta_y - pos_offset_y, map_rsc, entities)

                # Cancel all y movement
                else:
                    movement.speed.y = 0
                    # Try to continue moving in x direction
                    if not movement.speed.x == 0:
                        moveUntilCollision(entity, target_delta_x - pos_offset_x, 0, map_rsc, entities)

                # Call the collision handler
                if not collision_direction == CollisionDirection.Top:
                    if tile_collider.tileBottomLeftRightCollisionEventHandler is not None:
                        tile_collider.tileBottomLeftRightCollisionEventHandler(entity, collision_direction,
                                                                               (cell_x, cell_y), entities)
                else:
                    if tile_collider.tileTopCollisionEventHandler is not None:
                        tile_collider.tileTopCollisionEventHandler(entity, (cell_x, cell_y), entities)

                # Cancel all movement

                collided = True
                break

        if collided:
            break


class MovementSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))

        for entity in self.entities.get_with_component(MovementComponent, TransformComponent):
            movement: MovementComponent = entity
            transform: TransformComponent = entity
            movement.speed += movement.acceleration * time_rsc.deltaTime

            # No tile collision
            if not isinstance(entity, TileColliderComponent):
                transform.position += movement.speed * time_rsc.deltaTime
                return

            target_delta_position = movement.speed * time_rsc.deltaTime
            moveUntilCollision(entity, target_delta_position.x, target_delta_position.y, map_rsc, self.entities)

            # Above 0
            if transform.position.y < 0:
                if isinstance(entity, PlayerEntity):
                    next(self.entities.get_by_class(EventManagerResource)).emit_event(GameEndEventName.GameLost,
                                                                                      GameEndEvent(
                                                                                          GameEndEventType.GameLost))
                else:
                    self.entities.delete_buffer_add(entity)
