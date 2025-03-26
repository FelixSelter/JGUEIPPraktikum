from typing import Any

from ecs_pattern import entity, EntityManager
import pygame

from animation import AnimationComponent, Animation, AnimationFrame
from assets import Assets
from components.clickable_component import ClickableComponent
from components.gravity_component import GravityComponent
from components.hitbox_component import HitboxComponent
from components.movement_component import MovementComponent
from components.player_component import PlayerComponent
from components.score_component import ScoreComponent
from components.sprite_component import SpriteComponent
from components.tile_collider_component import TileColliderComponent
from components.transform_component import TransformComponent
from entities.coin_entity import CoinEntity
from entities.enemy_entity import EnemyEntity
from entities.power_up_entity import PowerUpEntity
from events import EventManagerResource
from events.game_end_event import GameEndEventName, GameEndEvent, GameEndEventType
from util import CollisionDirection
from util.additional_math import Vec2


@entity
class PlayerEntity(PlayerComponent, SpriteComponent, TransformComponent, MovementComponent, HitboxComponent, TileColliderComponent,
                   GravityComponent, ScoreComponent, AnimationComponent, ClickableComponent):
    def serialize(self):
        return PlayerData(self.position)


def playerCollisionHandler(player: PlayerEntity, other: Any, direction: CollisionDirection, entities: EntityManager):
    if isinstance(other, CoinEntity):
        if other.treasure == 42:
            pygame.mixer.Sound.play(Assets.get().eggCollection)
            print("You win!")
            next(entities.get_by_class(EventManagerResource)).emit_event(GameEndEventName.GameWon,
                                                                         GameEndEvent(GameEndEventType.GameWon))
        else:
            pygame.mixer.Sound.play(Assets.get().coinCollection)
            player.score += other.treasure
        entities.delete_buffer_add(other)

    if isinstance(other, PowerUpEntity):
        player.statusEffects.append([other.powerDelay, other.power])
        player.jump += other.power
        entities.delete_buffer_add(other)

    if isinstance(other, EnemyEntity):
        if direction == CollisionDirection.Top:
            player.speed.y = 10
            entities.delete_buffer_add(other)
        else:
            next(entities.get_by_class(EventManagerResource)).emit_event(GameEndEventName.GameLost,
                                                                         GameEndEvent(GameEndEventType.GameLost))


class PlayerData:
    def __init__(self, position: Vec2, left: int, right: int, jump: int):
        self.position = position
        self.left = left
        self.right = right
        self.jump = jump

    def deserialize(self):
        return PlayerEntity(
            key_up=self.jump,
            key_right=self.right,
            key_left=self.left,
            key_array={self.left: False, self.right: False},
            jump=15,
            position=self.position,
            width=1,
            height=1,
            sprite=Assets.get().playerImgs_right[0],
            acceleration=Vec2(0, 0),
            speed=Vec2(0, 0),
            maxspeed=8,
            hitboxEventHandler=playerCollisionHandler,
            tileBottomLeftRightCollisionEventHandler=None,
            tileTopCollisionEventHandler=None,
            score=0,
            animations={"right": Animation(
                [AnimationFrame(Assets.get().playerImgs_right[i], 0.3) for i in
                 range(len(Assets.get().playerImgs_right))]),
                "left": Animation(
                    [AnimationFrame(Assets.get().playerImgs_left[i], 0.3) for i in
                     range(len(Assets.get().playerImgs_left))])
            },
            activeAnimation="right",
            currentTime=0,
            loopAnimation=True,
            click_event_handler=None,
            statusEffects=[]
        )
