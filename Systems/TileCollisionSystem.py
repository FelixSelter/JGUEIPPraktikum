from enum import Enum
from math import floor, ceil

from ecs_pattern import System, EntityManager

from Components import HitboxComponent, TransformComponent, TileColliderComponent, MovementComponent, \
    TileCollisionDirection
from Resources import MapResource


class TileCollisionSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))

        for entity in self.entities.get_with_component(HitboxComponent, TransformComponent, MovementComponent):
            transform: TransformComponent = entity
            hitbox: HitboxComponent = entity
            tileCollider: TileColliderComponent = entity
            movement: MovementComponent = entity

            # Calculate tiles covered by hitbox

            minX, maxX = transform.position.x, transform.position.x + transform.width
            minY, maxY = transform.position.y, transform.position.y + transform.height
            for tileX in range(floor(minX), floor(maxX) + 1):
                for tileY in range(floor(minY), floor(maxY) + 1):
                    if not (0 <= tileY < len(map_rsc.solidTiles) and 0 <= tileX < len(map_rsc.solidTiles[tileY])):
                        continue

                    direction = None
                    if map_rsc.solidTiles[tileY][tileX]:
                        threshold = 0.25  # Prevents above and below to trigger if hit from the sides. Tune if gravity and jump speed etc change

                        # above
                        if tileY < minY < tileY + 1 and tileY + 1 - minY < threshold:
                            direction = TileCollisionDirection.Top
                            transform.position.y = tileY + transform.height
                            movement.speed.y = 0

                        # below
                        elif tileY < maxY < tileY + 1 and maxY - tileY < threshold:
                            direction = TileCollisionDirection.Bottom
                            transform.position.y = tileY - transform.height
                            movement.speed.y = 0

                        else:
                            # right
                            if tileX < minX < tileX + 1 and tileX + 1 - minX < threshold:
                                direction = TileCollisionDirection.Right
                                transform.position.x = tileX + transform.width
                                movement.speed.x = 0

                            # left
                            elif tileX < maxX < tileX + 1 and maxX - tileX < threshold:
                                direction = TileCollisionDirection.Left
                                transform.position.x = tileX - transform.width
                                movement.speed.x = 0

                    tileCollider.tileCollisionEventHandler(direction, self.entities)
