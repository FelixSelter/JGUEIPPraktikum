import os
import random

from ecs_pattern import SystemManager
import pygame
from pygame import Surface, Rect
from pygame_gui import TEXT_EFFECT_EXPAND_CONTRACT, UIManager
from pygame_gui.core import ObjectID
from pygame_gui.elements import UITextBox, UIButton, UIPanel
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu

from animation import AnimationSystem
from app import app
from events import EventParsingSystem, MouseEventName, KeyboardEventName, EventManagerResource, UiButtonEvent, \
    UiButtonEventName
from events.game_end_event import GameEndEventName
from map import Map, MapResource
from resources import CameraResource, TimeResource
from scenes import Scene
from scenes.leveleditor_scene import LevelEditorScene
from systems.parallax_system import ParallaxItem, ParallaxLayer, Range, ParallaxManager
from systems.entity_collision_system import EntityCollisionSystem
from systems.gravity_system import GravitySystem
from systems.movement_system import MovementSystem
from systems.death_system import DeathSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem



def preload_mainmenu_fonts(ui_manager: UIManager):
    ui_manager.add_font_paths("TitleFont", "rsc/fonts/RetroSigned.ttf")
    ui_manager.preload_fonts([
        {'name': 'freesans', 'point_size': 20, 'style': 'regular'},
        {'name': 'TitleFont', 'point_size': 100, 'style': 'regular'}
    ])

class MainMenuScene(Scene):
    camera_direction = 1

    def button_handler(self, event: UiButtonEvent):
        level = self.level_select.selected_option[0]
        if event.button == self.play_button:
            from scenes.game_scene import GameScene
            app.change_scene(GameScene(self.screen, f"rsc/Maps/{level}"))
        elif event.button == self.edit_button:
            app.change_scene(LevelEditorScene(self.screen, f"rsc/Maps/{level}"))
        elif event.button == self.new_button:
            app.change_scene(LevelEditorScene(self.screen, None))

    def __init__(self, screen: Surface):
        super().__init__(screen, "rsc/ui/mainmenu.json", preload_mainmenu_fonts)
        self.event_parsing_system = EventParsingSystem(screen, self.entities, {
            MouseEventName.MouseButtonUp: [],
            MouseEventName.MouseButtonDown: [],
            MouseEventName.MouseDragEnd: [],
            KeyboardEventName.KeyDown: [],
            KeyboardEventName.KeyUp: [],
            GameEndEventName.GameLost: [],
            GameEndEventName.GameWon: [],
            UiButtonEventName: [self.button_handler]
        })
        self.map = map
        self.screen = screen

        self.system_manager: SystemManager = SystemManager([
            self.event_parsing_system,
            TimeSystem(self.entities),
            MovementSystem(self.entities),
            EntityCollisionSystem(self.entities),
            GravitySystem(self.entities),
            DeathSystem(self.entities),
            AnimationSystem(self.entities),
            RenderingSystem(self.entities, screen)
        ])

        # Parallax Layers
        self.ParallaxManager = ParallaxManager(self.screen)
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        # Hintergrundbild
        self.BackgroundLayer = ParallaxItem(
            x=0, y=0,
            z_index=0,
            image=pygame.image.load("rsc/img/background/background.png").convert_alpha(),
            scale=(self.screen_width, self.screen_height)
        )
        self.ParallaxManager.add_object(self.BackgroundLayer)
        # Wolken
        self.CloudsLayer = ParallaxLayer(
            image_path="rsc/img/background/clouds.png",
            z_index=1,
            scale=Range(1.8, 2.0)
        )
        self.ParallaxManager.add_object(self.CloudsLayer)
        # Bäume
        self.TreeLayer = ParallaxLayer(
            image_path="rsc/img/background/trees.png",
            z_index=2,
            scale=Range(1.95, 2.05)
        )
        self.ParallaxManager.add_object(self.TreeLayer)
        # Büsche
        self.BushLayer = ParallaxLayer(
            image_path="rsc/img/background/bushes.png",
            z_index=3,
            scale=Range(1.45, 1.55)
        )
        self.ParallaxManager.add_object(self.BushLayer)

    def load(self):
        self.create_ui()
        m = Map.load("rsc/Maps/MainMenuMap.map")
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
        maps = sorted([file for file in os.listdir("rsc/Maps") if not file.endswith(".py")])
        panel = UIPanel(Rect(0, 50, 333, 233), manager=self.ui_manager, anchors={"center": "center"},
                        object_id=ObjectID(object_id="#panel"))
        self.level_select = UIDropDownMenu(maps, maps[0], Rect(0, 0, 300, 50), manager=self.ui_manager,
                                           container=panel)
        self.play_button = UIButton(Rect(0, 50, 300, 50), "Spielen", manager=self.ui_manager, container=panel)
        self.edit_button = UIButton(Rect(0, 100, 300, 50), "Level bearbeiten", manager=self.ui_manager, container=panel)
        self.new_button = UIButton(Rect(0, 150, 300, 50), "Neues Level", manager=self.ui_manager, container=panel)

        # title_box = UITextBox(
        #     html_text="<effect id=title>Super Chicken 16</effect>",
        #     relative_rect=pygame.Rect(0, 20, self.screen.width, self.screen.height),
        #     manager=self.ui_manager, object_id=ObjectID(object_id="#title"))
        # title_box.set_active_effect(TEXT_EFFECT_EXPAND_CONTRACT, effect_tag="title")

    def start(self):
        super().start()

        # Wolken
        x: int = 0
        while x < self.screen_width * 2:
            scale = self.CloudsLayer.add_item(x)
            x += scale[0] / 2

        # Bäume
        tree_width = self.TreeLayer.image.get_width() * 2.0
        x = 0
        while x < self.screen_width * 3:
            group_size = random.choice([1, 2]) if random.random() < 0.85 else 1
            for i in range(group_size):
                y_offset = random.randint(360, 370)  # Bodennahe Y-Position
                self.TreeLayer.add_item(x + i * tree_width * 0.9, y_offset)
            x += tree_width * group_size + random.randint(100, 300)

        # Büsche
        bush_width = self.BushLayer.image.get_width() * 1.5
        x = 0
        while x < self.screen_width * 3:
            if random.random() < 0.6:
                y_offset = random.randint(395, 410)  # Bodennahe Y-Position
                self.BushLayer.add_item(x, y_offset)
            x += bush_width + random.randint(100, 300)

    def update(self):
        camera_rsc: CameraResource = next(self.entities.get_by_class(CameraResource))
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))
        self.ParallaxManager.update(0.1, 0)

        camera_rsc.x += self.camera_direction * 0.5 * time_rsc.deltaTime
        if not (0 <= camera_rsc.x <= map_rsc.map.width - camera_rsc.screenWidthInTiles):
            self.camera_direction = -self.camera_direction
        super().update()
