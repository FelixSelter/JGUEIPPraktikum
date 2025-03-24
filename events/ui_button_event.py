from pygame_gui.elements import UIButton

from events import Event

UiButtonEventName = "UiButtonClick"


class UiButtonEvent(Event):
    def __init__(self, button: UIButton):
        self.button = button
