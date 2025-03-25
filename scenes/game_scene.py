import pygame
from ecs_pattern import SystemManager
from pygame import Surface, Rect
from pygame_gui import TEXT_EFFECT_TYPING_APPEAR, TEXT_EFFECT_FADE_IN, TEXT_EFFECT_BOUNCE, TEXT_EFFECT_TILT, \
    TEXT_EFFECT_EXPAND_CONTRACT
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UIButton, UIPanel

from animation import AnimationSystem
from assets import Assets
from entities.player_entity import PlayerEntity
from events import EventParsingSystem, MouseEventName, KeyboardEventName, EventManagerResource
from events.game_end_event import GameEndEvent, GameEndEventType, GameEndEventName
from map import Map, MapResource
from resources import CameraResource, TimeResource
from scenes import Scene
from systems.click_event_system import ClickEventSystem
from systems.spawner_system import SpawnerSystem
from systems.camera_movement_system import CameraMovementSystem
from systems.entity_collision_system import EntityCollisionSystem
from systems.control_system import ControllerSystem
from systems.gravity_system import GravitySystem
from systems.movement_system import MovementSystem
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem


class GameScene(Scene):

    def game_end_handler(self, event: GameEndEvent):
        if event.event_type == GameEndEventType.GameLost:
            self.loose_panel.show()
        else:
            self.win_panel.show()

        for player_entity in self.entities.get_by_class(PlayerEntity):
            self.entities.delete_buffer_add(player_entity)

    def __init__(self, screen: Surface, map: str):
        super().__init__(screen, "rsc/ui/gamescene.json")
        click_event_system = ClickEventSystem(self.entities, None)
        controller_system = ControllerSystem(self.entities, pygame.event.get)
        self.event_parsing_system = EventParsingSystem(screen, self.entities, {
            MouseEventName.MouseButtonUp: [click_event_system.click_event_handler],
            MouseEventName.MouseButtonDown: [click_event_system.click_event_handler],
            MouseEventName.MouseDragEnd: [click_event_system.click_event_handler, self.game_end_handler],
            KeyboardEventName.KeyDown: [controller_system.keypress_event_handler],
            KeyboardEventName.KeyUp: [controller_system.keypress_event_handler],
            GameEndEventName.GameLost: [self.game_end_handler],
            GameEndEventName.GameWon: [self.game_end_handler]
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
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            CameraMovementSystem(self.entities, screen),
            RenderingSystem(self.entities, screen),
            SpawnerSystem(self.entities)
        ])

    def load(self):
        self.create_ui()

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

    def create_ui(self):
        self.win_panel = UIPanel(Rect(0, 0, self.screen.width, self.screen.height), manager=self.ui_manager,
                                 visible=False, object_id=ObjectID(class_id="@panel"))

        win_text = UITextBox(
            f'<font face=noto_sans pixel_size=30 color=#000000><effect id=eff1>Du hast gewonnen!</effect></font><br><br><effect id="eff2"><font color=#000000 pixel_size=20>Deine Zeit: <body bgcolor=#990000>00:00:00</body><br>Erreichte Punkte: <body bgcolor=#990000>100</body></font></effect>',
            Rect((0, -self.screen.height // 5),
                 (self.screen.width // 3, self.screen.height // 3)),
            anchors={"center": "center"},
            manager=self.ui_manager,
            container=self.win_panel.get_container(),
            object_id=ObjectID(class_id="@textbox",
                               object_id="#textbox-win"))
        win_text.set_active_effect(TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='eff1')
        win_text.set_active_effect(TEXT_EFFECT_TYPING_APPEAR, effect_tag='eff2')

        UIButton(
            Rect(0, -self.screen.height // 5 + 80, self.screen.width // 6, 30), "Menü",
            manager=self.ui_manager, anchors={"center": "center"}, container=self.win_panel.get_container())

        self.loose_panel = UIPanel(Rect(0, 0, self.screen.width, self.screen.height), manager=self.ui_manager,
                                   visible=False, object_id=ObjectID(class_id="@panel"))

        loose_text = UITextBox(
            f'<font face=noto_sans pixel_size=30 color=#000000><effect id=eff1>Du hast verloren :(</effect></font><br><br><effect id="eff2"><font color=#000000 pixel_size=20>Deine Zeit: <body bgcolor=#990000>00:00:00</body><br>Erreichte Punkte: <body bgcolor=#990000>100</body></font></effect>',
            Rect((0, -self.screen.height // 5),
                 (self.screen.width // 3, self.screen.height // 3)),
            anchors={"center": "center"},
            manager=self.ui_manager,
            container=self.loose_panel.get_container(),
            object_id=ObjectID(class_id="@textbox",
                               object_id="#textbox-win"))
        loose_text.set_active_effect(TEXT_EFFECT_EXPAND_CONTRACT, effect_tag='eff1')
        loose_text.set_active_effect(TEXT_EFFECT_TYPING_APPEAR, effect_tag='eff2')

        UIButton(
            Rect(0, -self.screen.height // 5 + 80, self.screen.width // 6, 30), "Menü",
            manager=self.ui_manager, anchors={"center": "center"}, container=self.loose_panel.get_container())

    def start(self):
        super().start()
        pygame.mixer.Sound.play(Assets.get().backgroundMusic)
