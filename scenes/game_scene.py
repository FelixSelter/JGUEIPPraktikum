from math import floor

import pygame
from ecs_pattern import SystemManager
from pygame import Surface, Rect
from pygame_gui import TEXT_EFFECT_TYPING_APPEAR, TEXT_EFFECT_EXPAND_CONTRACT
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UIButton

from animation import AnimationSystem
from app import app
from timed_action import TimedActionSystem
from entities.player_entity import PlayerEntity
from events import EventParsingSystem, MouseEventName, KeyboardEventName, EventManagerResource, UiButtonEventName
from events.game_end_event import GameEndEvent, GameEndEventType, GameEndEventName
from map import Map, MapResource
from resources import CameraResource, TimeResource
from scenes import Scene
from scenes.mainmenu_scene import MainMenuScene
from systems.click_event_system import ClickEventSystem
from systems.power_up_system import PowerUpSystem
from systems.camera_movement_system import CameraMovementSystem
from systems.entity_collision_system import EntityCollisionSystem
from systems.control_system import ControllerSystem
from systems.gravity_system import GravitySystem
from systems.movement_system import MovementSystem
from systems.death_system import DeathSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem
from util.additional_math import fract


class GameScene(Scene):

    def game_end_handler(self, event: GameEndEvent):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        treasure_sum = 0
        for player_entity in self.entities.get_by_class(PlayerEntity):
            self.entities.delete_buffer_add(player_entity)
            treasure_sum += player_entity.score

        minutes = int(time_rsc.totalTime // 60)
        seconds = int(time_rsc.totalTime % 60)
        milliseconds = round(fract(time_rsc.totalTime) * 100)
        text = UITextBox(
            f'<font face=noto_sans pixel_size=30 color=#000000><effect id=eff1>Du hast {"gewonnen !!!" if event.event_type == GameEndEventType.GameWon else "verloren :("}!</effect></font><br><br><effect id="eff2"><font color=#000000 pixel_size=20>Deine Zeit: <body bgcolor=#990000>{minutes}:{seconds},{milliseconds}</body><br>Erreichte Punkte: <body bgcolor=#990000>{treasure_sum}</body></font></effect>',
            Rect((0, -self.screen.height // 5),
                 (self.screen.width // 3, self.screen.height // 3)),
            anchors={"center": "center"},
            manager=self.ui_manager,
            object_id=ObjectID(class_id="@textbox"))
        text.set_active_effect(TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='eff1')
        text.set_active_effect(TEXT_EFFECT_TYPING_APPEAR, effect_tag='eff2')

        UIButton(
            Rect(0, -self.screen.height // 5 + 80, self.screen.width // 6, 30), "Menü",
            manager=self.ui_manager, anchors={"center": "center"})

    def menu_button_listener(self, _):
        app.change_scene(MainMenuScene(app.screen))

    def __init__(self, screen: Surface, map: str):
        super().__init__(screen, "rsc/ui/gamescene.json")
        click_event_system = ClickEventSystem(self.entities, None)
        controller_system = ControllerSystem(self.entities, pygame.event.get)
        self.event_parsing_system = EventParsingSystem(screen, self.entities, {
            MouseEventName.MouseButtonUp: [click_event_system.click_event_handler],
            MouseEventName.MouseButtonDown: [click_event_system.click_event_handler],
            MouseEventName.MouseDragEnd: [click_event_system.click_event_handler],
            KeyboardEventName.KeyDown: [controller_system.keypress_event_handler],
            KeyboardEventName.KeyUp: [controller_system.keypress_event_handler],
            GameEndEventName.GameLost: [self.game_end_handler],
            GameEndEventName.GameWon: [self.game_end_handler],
            UiButtonEventName: [self.menu_button_listener]
        })
        self.map = map
        self.screen = screen

        self.system_manager: SystemManager = SystemManager([
            self.event_parsing_system,
            TimeSystem(self.entities),
            click_event_system,
            controller_system,
            MovementSystem(self.entities),
            EntityCollisionSystem(self.entities),
            GravitySystem(self.entities),
            DeathSystem(self.entities),
            AnimationSystem(self.entities),
            CameraMovementSystem(self.entities, screen),
            RenderingSystem(self.entities, screen),
            PowerUpSystem(self.entities),
            TimedActionSystem(self.entities)
        ])

    def load(self):
        m = Map.load(self.map)
        tiles, entities = m.parse()

        self.entities.add(
            EventManagerResource(
                emit_event=self.event_parsing_system.emit_event
            ),
            TimeResource(
                totalTime=0,
                deltaTime=0,
                paused=False,
                doUnPause=False,
            ),
            CameraResource(
                screenWidthInTiles=16,  # * 2,
                screenHeightInTiles=9,  # * 2,
                x=0,
                y=0,
                ui_manager=self.ui_manager
            ),
            MapResource(
                map=m
            ),
            *tiles,
            *entities

        )

    def start(self):
        super().start()
