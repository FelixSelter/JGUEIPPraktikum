import sys
from math import sqrt
from typing import Callable, List, Dict, Any

import pygame
from ecs_pattern import System, EntityManager
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, Surface, QUIT


class Event:
    canceled: bool = False


from events.mouse_event import MouseEvent, MouseEventType, MouseButton, MouseEventName
from events.keyboard_event import KeyboardEvent, KeyboardEventName, KeyboardEventType


class EventParsingSystem(System):
    min_drag_distance = 3

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
        for event in pygame.event.get():

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
                            self.emit_event(MouseEventName.MouseDragEnd,
                                            MouseEvent(self.screen, self.entities, MouseButton(i),
                                                       MouseEventType.DragEnd, start_pos,
                                                       mouse_pos))

                        self.emit_event(MouseEventName.MouseButtonUp,
                                        MouseEvent(self.screen, self.entities, MouseButton(i),
                                                   MouseEventType.Released, mouse_pos,
                                                   mouse_pos))

                        self.mouse_button_state[i] = (False, mouse_pos)
