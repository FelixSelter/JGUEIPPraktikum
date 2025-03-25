from math import floor
from random import randint

import pygame.event
from ecs_pattern import SystemManager
from pygame import Surface, Rect
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIScrollingContainer, UIButton

from animation import AnimationSystem
from entities.coin_entity import CoinData
from entities.player_entity import PlayerData, PlayerEntity
from entities.spawner_entity import SpawnerData
from entities.tile_entity import TileEntity
from events import EventParsingSystem, MouseEventName, KeyboardEventName, MouseEvent, UiButtonEventName, UiButtonEvent, \
    MouseButton
from map import Map, MapResource, Tiles
from resources import CameraResource, TimeResource
from scenes import Scene
from systems.click_event_system import ClickEventSystem
from systems.leveleditor_control_system import LevelEditorControlSystem
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem
from util.additional_math import Vec2


class LevelEditorScene(Scene):
    current_item = None
    placed_player = False

    def entity_click_handler(self, entity):
        self.entities.delete_buffer_add(entity)

    def button_click_handler(self, event: UiButtonEvent):
        if "#sliding_button" in event.button.object_ids:
            return
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))
        if event.button == self.save_button:
            map_rsc.map.save(f"{randint(0, 100)}.map")
            exit()

        self.current_item = event.button.object_ids[1][8:]

    def place_tile(self, event: MouseEvent):
        # Make the map as large as the clicked area
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))
        while map_rsc.map.height <= floor(event.world_start_pos.y):
            map_rsc.map.tiles.append([])
            map_rsc.map.height += 1
        map_rsc.map.width = max(map_rsc.map.width, floor(event.world_start_pos.x) + 1)
        for row in map_rsc.map.tiles:
            while len(row) < map_rsc.map.width:
                row.append(Tiles.Air)

        # Set the tile
        tilemap_x, tilemap_y = floor(event.world_start_pos.x), floor(
            event.world_start_pos.y)

        if event.button == MouseButton.Left:
            if not map_rsc.map.tiles[tilemap_y][tilemap_x] == Tiles.Air:
                return

            tile = Tiles(self.current_item)

            map_rsc.map.tiles[tilemap_y][tilemap_x] = tile

            self.entities.add(TileEntity(
                position=Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y)),
                width=1,
                height=1,
                sprite=tile.getSprite()
            ))

        # Delete the tile
        else:
            map_rsc.map.tiles[tilemap_y][tilemap_x] = Tiles.Air
            for tile in self.entities.get_by_class(TileEntity):
                if tile.position.x == floor(event.world_start_pos.x) and tile.position.y == floor(
                        event.world_start_pos.y):
                    self.entities.delete_buffer_add(tile)

    def place_entity(self, event: MouseEvent):
        map_rsc: MapResource = next(self.entities.get_by_class(MapResource))
        match self.current_item:
            case "player":
                if self.placed_player:
                    return
                self.placed_player = True
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = PlayerData(pos)
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "coin":
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = CoinData(pos, 1, "Coin")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "shit":
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = CoinData(pos, -1, "Shit")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "mushroom":
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = CoinData(pos, 10, "Mushroom")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "egg":
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = CoinData(pos, 1, "Egg")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "spawner-pig":
                pos = Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y))
                d = SpawnerData(pos, 5, "Pig")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "spawner-cow":
                pos = Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y))
                d = SpawnerData(pos, 5, "Cow")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "spawner-sheep":
                pos = Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y))
                d = SpawnerData(pos, 5, "Sheep")
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)
            case "player":
                pos = Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y))
                d = PlayerEntity(pos)
                map_rsc.map.entity_data.append(d)
                e = d.deserialize()
                e.click_event_handler = self.entity_click_handler
                self.entities.add(e)

    def space_click_handler(self, event: MouseEvent):
        if self.current_item is None:
            return

        if self.current_item in [tile.value for tile in Tiles]:
            self.place_tile(event)
        else:
            self.place_entity(event)

    def __init__(self, screen: Surface, map: str | None):
        super().__init__(screen, "rsc/ui/leveleditor.json")
        self.screen = screen
        self.map = map

        click_event_system = ClickEventSystem(self.entities, self.space_click_handler)
        control_system = LevelEditorControlSystem(self.entities, pygame.event.get())

        self.system_manager: SystemManager = SystemManager([
            EventParsingSystem(screen, self.entities, {
                MouseEventName.MouseButtonUp: [click_event_system.click_event_handler],
                MouseEventName.MouseButtonDown: [click_event_system.click_event_handler],
                MouseEventName.MouseDragEnd: [click_event_system.click_event_handler],
                KeyboardEventName.KeyDown: [control_system.keypress_event_handler],
                KeyboardEventName.KeyUp: [control_system.keypress_event_handler],
                UiButtonEventName: [self.button_click_handler]
            }),
            click_event_system,
            control_system,
            TimeSystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            RenderingSystem(self.entities, screen)
        ])

    def create_ui(self):
        scrolling_container = UIScrollingContainer(Rect(self.screen.width - 86, 0, 86, self.screen.height),
                                                   allow_scroll_x=False,
                                                   should_grow_automatically=False, manager=self.ui_manager)
        i = 0
        for tile in Tiles:
            if tile == Tiles.Air:
                continue
            UIButton(Rect(0, i * 66, 66, 66), "",
                     manager=self.ui_manager,
                     container=scrolling_container,
                     object_id=ObjectID(class_id="@button-leveleditor", object_id=f"#button-{tile.value}"),
                     tool_tip_text=tile.value)
            i += 1

        for obj in ["coin", "shit", "mushroom", "egg", "spawner-pig", "spawner-cow", "spawner-sheep", "player"]:
            UIButton(Rect(0, i * 66, 66, 66), "",
                     manager=self.ui_manager,
                     container=scrolling_container,
                     object_id=ObjectID(class_id="@button-leveleditor", object_id=f"#button-{obj}"),
                     tool_tip_text=obj)
            i += 1

        self.save_button = UIButton(Rect(0, i * 66, 66, 66), "Save",
                                    manager=self.ui_manager,
                                    container=scrolling_container)

        scrolling_container.set_scrollable_area_dimensions((86, (i + 1) * 66))

    def load(self):
        self.create_ui()

        m = Map([], []) if self.map is None else Map.load(self.map)
        tiles, entities = m.parse()

        for entity in entities:
            entity.click_event_handler = self.entity_click_handler

        self.entities.add(
            TimeResource(
                totalTime=0,
                deltaTime=0,
                paused=False,
                doUnPause=False,
            ),
            CameraResource(
                screenWidthInTiles=16 * 2,
                screenHeightInTiles=9 * 2,
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
