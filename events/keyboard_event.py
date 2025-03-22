from enum import Enum

from events import Event


# Events emitted by the event system
class KeyboardEventName(Enum):
    KeyDown = "KeyboardKeyDown"
    KeyUp = "KeyboardKeyUp"


class KeyboardEventType(Enum):
    KeyDown = 0
    KeyUp = 1


class KeyboardEvent(Event):
    def __init__(self, event_type: KeyboardEventType, key: int):
        self.event_type = event_type
        self.key = key
