import sys
from copy import copy
from math import sqrt
from typing import Callable, List, Dict, Any

import pygame
from ecs_pattern import System, EntityManager, entity
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, Surface, QUIT
from pygame_gui import UI_BUTTON_PRESSED, UI_FILE_DIALOG_PATH_PICKED, UI_WINDOW_CLOSE

from resources import CameraResource


class Event:
    canceled: bool = False


from events.mouse_event import MouseEvent, MouseEventType, MouseButton, MouseEventName
from events.keyboard_event import KeyboardEvent, KeyboardEventName, KeyboardEventType
from events.ui_button_event import UiButtonEventName, UiButtonEvent
from events.file_picker_event import FilePickerEventName, FilePickerEvent, FilePickerEventType


@entity
class EventManagerResource:
    emit_event: Callable[[Any, Event], None]  # emit_event(event_name, event)


class EventParsingSystem(System):
    min_drag_distance = 3
    delayed_events = []
    i = 0

    def __init__(self, screen: Surface, entities: EntityManager,
                 event_handlers: Dict[Any, List[Callable[[Event], None]]]):
        self.screen = screen
        self.entities = entities
        self.event_handlers = event_handlers

        mouse_pos = pygame.mouse.get_pos()
        self.mouse_button_state = [(button_state, mouse_pos) for button_state in pygame.mouse.get_pressed()]

    def emit_event(self, event_type: Any, event: Event):
        if event_type not in self.event_handlers:
            return

        for handler in self.event_handlers[event_type]:
            if event.canceled:
                break
            handler(event)

    def update(self):
        self.i += 1
        camera: CameraResource = next(self.entities.get_with_component(CameraResource))

        # Delay events so click can be cancelled by ui click
        delayed_events = copy(self.delayed_events)
        self.delayed_events.clear()

        was_ui_click = False
        picked_file_dialogs = []
        for event in pygame.event.get():
            camera.ui_manager.process_events(event)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                key = getattr(event, 'key', None)
                self.emit_event(KeyboardEventName.KeyDown, KeyboardEvent(KeyboardEventType.KeyDown, key))

            elif event.type == pygame.KEYUP:
                key = getattr(event, 'key', None)
                self.emit_event(KeyboardEventName.KeyUp, KeyboardEvent(KeyboardEventType.KeyUp, key))

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_button_state = pygame.mouse.get_pressed()
                for i in range(len(mouse_button_state)):
                    if mouse_button_state[i] is True and self.mouse_button_state[i][0] is False:
                        self.emit_event(MouseEventName.MouseButtonDown,
                                        MouseEvent(self.screen, self.entities, MouseButton(i), MouseEventType.Pressed,
                                                   mouse_pos,
                                                   mouse_pos))
                        self.mouse_button_state[i] = (True, mouse_pos)

            elif event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                mouse_button_state = pygame.mouse.get_pressed()
                for i in range(len(mouse_button_state)):
                    if mouse_button_state[i] is False and self.mouse_button_state[i][0] is True:
                        start_pos = self.mouse_button_state[i][1]

                        # Send additional drag event
                        if sqrt((start_pos[0] - mouse_pos[0]) ** 2 + (
                                start_pos[1] - mouse_pos[1]) ** 2) > self.min_drag_distance:
                            self.delayed_events.append((MouseEventName.MouseDragEnd,
                                                        MouseEvent(self.screen, self.entities, MouseButton(i),
                                                                   MouseEventType.DragEnd, start_pos,
                                                                   mouse_pos)))

                        self.delayed_events.append((MouseEventName.MouseButtonUp,
                                                    MouseEvent(self.screen, self.entities, MouseButton(i),
                                                               MouseEventType.Released, mouse_pos,
                                                               mouse_pos)))

                        self.mouse_button_state[i] = (False, mouse_pos)

            elif event.type == UI_BUTTON_PRESSED:
                self.emit_event(UiButtonEventName, UiButtonEvent(event.ui_element))
                was_ui_click = True

            elif event.type == UI_FILE_DIALOG_PATH_PICKED:
                picked_file_dialogs.append(event.ui_element)
                self.emit_event(FilePickerEventName.FilePicked,
                                FilePickerEvent(FilePickerEventType.FilePicked, event.ui_element, event.text))

            elif event.type == UI_WINDOW_CLOSE:
                if event.ui_element not in picked_file_dialogs:
                    self.emit_event(FilePickerEventName.Aborted,
                                    FilePickerEvent(FilePickerEventType.Aborted, event.ui_element, None))

        if not was_ui_click:
            for name, event in delayed_events:
                self.emit_event(name, event)
