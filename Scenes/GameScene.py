from typing import Any

import pygame
from ecs_pattern import SystemManager, EntityManager
from pygame import Surface

from Entities import CoinEntity, PlayerEntity
from Animation import Animation, AnimationFrame, AnimationSystem
from Map import Map, MapResource
from Resources import CameraResource, TimeResource
from Scenes import Scene
from Systems.CameraMovementSystem import CameraMovementSystem
from Systems.CollisionSystem import CollisionSystem
from Systems.ControlSystem import ControllerSystem
from Systems.GravitySystem import GravitySystem
from Systems.MovementSystem import MovementSystem
from Systems.PurgeDeleteBufferSystem import PurgeDeleteBufferSystem
from Systems.RenderingSystem import RenderingSystem
from Systems.TileCollisionSystem import TileCollisionSystem
from Systems.TimeSystem import TimeSystem
from Assets import Assets
from util.math import Vec2


def playerCollisionHandler(player: PlayerEntity, item: Any, entities: EntityManager):
    if isinstance(item, CoinEntity):
        player.score += item.treasure
        entities.delete_buffer_add(item)


class GameScene(Scene):
    def __init__(self, screen: Surface):
        self.system_manager: SystemManager = SystemManager([
            TimeSystem(self.entities),
            ControllerSystem(self.entities, pygame.event.get),
            MovementSystem(self.entities),
            TileCollisionSystem(self.entities),
            CollisionSystem(self.entities),
            GravitySystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            CameraMovementSystem(self.entities, screen),
            RenderingSystem(self.entities, screen)
        ])

    def load(self):
        map = Map.load("rsc/Maps/Level1")
        tiles = map.parse()

        self.entities.add(
            TimeResource(
                totalTime=0,
                deltaTime=0,
                paused=False,
                doUnPause=False,
            ),
            CameraResource(
                screenWidthInTiles=16,
                screenHeightInTiles=9,
                x=0,
                y=0
            ),
            MapResource(
                map=map
            ),
            *tiles,
            PlayerEntity(
                position=Vec2(3, 8),
                width=1,
                height=1,
                sprite=Assets.get().playerImgs[0],
                acceleration=Vec2(0, 0),
                speed=Vec2(0, 0),
                hitboxEventHandler=playerCollisionHandler,
                tileCollisionEventHandler=lambda _a, _b, _c: None,
                score=0,
                animations={"default": Animation(
                    [AnimationFrame(Assets.get().playerImgs[0], 0.3), AnimationFrame(Assets.get().playerImgs[1], 0.3),
                     AnimationFrame(Assets.get().playerImgs[2], 0.3)])},
                activeAnimation="default",
                currentTime=0,
                loopAnimation=True
            ),
            CoinEntity(
                position=Vec2(5.25, 3.25),
                width=0.5,
                height=0.5,
                sprite=Assets.get().coinImg,
                hitboxEventHandler=lambda _a, _b, _c: None,
                treasure=1
            )
        )
