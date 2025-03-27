from math import floor

from ecs_pattern import entity, EntityManager

from assets import Assets
from entities.bunnyegg_entity import BunnyEggEntity, BunnyEggAction
from map import MapResource
from resources import CameraResource, TimeResource
from timed_action import TimedActionComponent, TimedAction
from components.clickable_component import ClickableComponent
from components.gravity_component import GravityComponent
from components.health_component import HealthComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from util.additional_math import Vec2

from random import shuffle, random


@entity
class BunnyEntity(SpriteComponent, TransformComponent, HitboxComponent, ClickableComponent, GravityComponent,
                  MovementComponent, TileColliderComponent, HealthComponent, TimedActionComponent):

    def serialize(self):
        return BunnyData(self.position)


def find_free_tiles(bunny: BunnyEntity, entities: EntityManager):
    map_rsc: MapResource = next(entities.get_by_class(MapResource))
    camera_rsc: CameraResource = next(entities.get_by_class(CameraResource))

    tiles = []
    # For every x on screen, find an air tile with ground below
    for x in range(floor(camera_rsc.x), floor(camera_rsc.x) + camera_rsc.screenWidthInTiles):
        has_ground = False
        for y in range(floor(camera_rsc.y), floor(camera_rsc.y) + camera_rsc.screenHeightInTiles):
            if not (0 <= x < map_rsc.map.width and 0 <= y < map_rsc.map.height):
                if has_ground:
                    tiles.append(Vec2(x, y))
                    has_ground = False
                continue
            if map_rsc.map.tiles[y][x].isSolid():
                has_ground = True
            elif has_ground:
                tiles.append(Vec2(x, y))
                has_ground = False

    return tiles


class SpawnReinforcementsAttack(TimedAction):
    def __init__(self):
        super().__init__(attack_delay=5)

    def execute_action(self, bunny: BunnyEntity, entities: EntityManager):
        camera_rsc: CameraResource = next(entities.get_by_class(CameraResource))
        tiles = find_free_tiles(bunny, entities)
        shuffle(tiles)
        for i in range(min(len(tiles), 4)):
            time_rsc: TimeResource = next(entities.get_by_class(TimeResource))
            action = BunnyEggAction()
            action.last_attack_time = time_rsc.totalTime
            entities.add_buffer.append(BunnyEggEntity(
                sprite=Assets.get().eggImgs[0],
                position=Vec2(tiles[i].x, camera_rsc.y + camera_rsc.screenHeightInTiles + random()),
                width=1,
                height=1,
                speed=Vec2(0, 0),
                acceleration=Vec2(0, 0),
                hitboxEventHandler=None,
                tileBottomLeftRightCollisionEventHandler=None,
                tileTopCollisionEventHandler=None,
                actions=[action]
            ))


class TeleportAttack(TimedAction):
    def __init__(self):
        super().__init__(attack_delay=2)

    def execute_action(self, bunny: BunnyEntity, entities: EntityManager):
        tiles = find_free_tiles(bunny, entities)
        shuffle(tiles)
        if len(tiles) > 0:
            bunny.position = tiles[0]


class BunnyData:
    def __init__(self, position: Vec2):
        self.position = position

    def deserialize(self):
        return BunnyEntity(
            position=self.position,
            width=1,
            height=1,
            health=3,
            speed=Vec2(0, 0),
            acceleration=Vec2(0, 0),
            sprite=Assets.get().bunnyImg,
            hitboxEventHandler=None,
            click_event_handler=None,
            tileBottomLeftRightCollisionEventHandler=None,
            tileTopCollisionEventHandler=None,
            actions=[SpawnReinforcementsAttack(), TeleportAttack()]
        )
