from enum import Enum

from pygame_gui.elements import UIButton

from events import Event


class GameEndEventName(Enum):
    GameLost = "GameLost"
    GameWon = "GameWon"


class GameEndEventType(Enum):
    GameLost = "GameLost"
    GameWon = "GameWon"


class GameEndEvent(Event):
    def __init__(self, event_type: GameEndEventType):
        self.event_type = event_type
