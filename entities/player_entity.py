from typing import Any

from ecs_pattern import entity, EntityManager
import pygame

from animation import AnimationComponent, Animation, AnimationFrame
from assets import Assets
from components.clickable_component import ClickableComponent
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.score_component import ScoreComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from entities.coin_entity import CoinEntity
from entities.enemy_entity import EnemyEntity
from util import CollisionDirection
from util.additional_math import Vec2


@entity
class PlayerEntity(SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent, ScoreComponent, AnimationComponent, ClickableComponent):
    def serialize(self):
        return PlayerData(self.position)


def playerCollisionHandler(player: PlayerEntity, other: Any, direction: CollisionDirection, entities: EntityManager):
    if isinstance(other, CoinEntity):
        if other.treasure == 42:
            pygame.mixer.Sound.play(Assets.get().eggCollection)
            print("You win!")
        else:
            pygame.mixer.Sound.play(Assets.get().coinCollection)
            player.score += other.treasure
        entities.delete_buffer_add(other)

    if isinstance(other, EnemyEntity):
        if direction == CollisionDirection.Top:
            player.speed.y = 10
            entities.delete_buffer_add(other)
        else:
            entities.delete_buffer_add(player)
            #exit()


class PlayerData:
    def __init__(self, position: Vec2):
        self.position = position

    def deserialize(self):
        return PlayerEntity(
            position=self.position,
            width=1,
            height=1,
            sprite=Assets.get().playerImgs_right[0],
            acceleration=Vec2(0, 0),
            speed=Vec2(0, 0),
            hitboxEventHandler=playerCollisionHandler,
            tileBottomLeftRightCollisionEventHandler=None,
            tileTopCollisionEventHandler=None,
            score=0,
            animations={"right": Animation(
                [AnimationFrame(Assets.get().playerImgs_right[i], 0.3) for i in range(len(Assets.get().playerImgs_right))]),
                "left": Animation(
                [AnimationFrame(Assets.get().playerImgs_left[i], 0.3) for i in range(len(Assets.get().playerImgs_left))])
                },
            activeAnimation="right",
            currentTime=0,
            loopAnimation=True,
            click_event_handler=None
        )
