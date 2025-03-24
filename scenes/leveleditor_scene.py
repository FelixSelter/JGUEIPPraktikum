from math import floor
from random import randint

from ecs_pattern import SystemManager
from pygame import Surface, Rect
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIScrollingContainer, UIButton

from animation import AnimationSystem
from entities.coin_entity import CoinData
from entities.spawner_entity import SpawnerData
from entities.tile_entity import TileEntity
from events import EventParsingSystem, MouseEventName, KeyboardEventName, MouseEvent, UiButtonEventName, UiButtonEvent, \
    MouseButton
from map import Map, MapResource, Tiles
from resources import CameraResource, TimeResource
from scenes import Scene
from systems.click_event_system import ClickEventSystem
from systems.purge_delete_buffer_system import PurgeDeleteBufferSystem
from systems.rendering_system import RenderingSystem
from systems.time_system import TimeSystem
from util.additional_math import Vec2


class LevelEditorScene(Scene):
    current_item = None

    def entity_click_handler(self, entity):
        self.entities.delete_buffer_add(entity)

    def button_click_handler(self, event: UiButtonEvent):
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
        for row in map_rsc.map.tiles:
            while len(row) <= floor(event.world_start_pos.x):
                row.append(Tiles.Air)
        map_rsc.map.width = max(map_rsc.map.width, floor(event.world_start_pos.x) + 1)

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
            case "coin":
                pos = Vec2(floor(event.world_start_pos.x) + 0.25, floor(event.world_start_pos.y) + 0.25)
                d = CoinData(pos, 1, "Coin")
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
            case "spawner":
                pos = Vec2(floor(event.world_start_pos.x), floor(event.world_start_pos.y))
                d = SpawnerData(pos, 5, "Sheep")
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

    def __init__(self, screen: Surface):
        super().__init__(screen, "rsc/ui/leveleditor.json")
        self.screen = screen

        click_event_system = ClickEventSystem(self.entities, self.space_click_handler)

        self.system_manager: SystemManager = SystemManager([
            EventParsingSystem(screen, self.entities, {
                MouseEventName.MouseButtonUp: [click_event_system.click_event_handler],
                MouseEventName.MouseButtonDown: [click_event_system.click_event_handler],
                MouseEventName.MouseDragEnd: [click_event_system.click_event_handler],
                KeyboardEventName.KeyDown: [],
                KeyboardEventName.KeyUp: [],
                UiButtonEventName: [self.button_click_handler]
            }),
            click_event_system,
            TimeSystem(self.entities),
            PurgeDeleteBufferSystem(self.entities),
            AnimationSystem(self.entities),
            RenderingSystem(self.entities, screen)
        ])

    def create_ui(self):
        scrolling_container = UIScrollingContainer(Rect(self.screen.width - 86, 0, 86, self.screen.height),
                                                   allow_scroll_x=False,
                                                   should_grow_automatically=False)
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

        for obj in ["coin", "egg", "spawner"]:
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

        m = Map([], [])

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
            )
        )
