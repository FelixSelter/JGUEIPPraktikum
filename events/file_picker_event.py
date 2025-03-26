from enum import Enum

from pygame_gui.windows import UIFileDialog

from events import Event


class FilePickerEventName(Enum):
    FilePicked = "FilePicked"
    Aborted = "FileChooseAborted"


class FilePickerEventType(Enum):
    FilePicked = "FilePicked"
    Aborted = "FileChooseAborted"


class FilePickerEvent(Event):
    def __init__(self, event_type: FilePickerEventType, dialog: UIFileDialog, file: str | None):
        self.event_type = event_type
        self.dialog = dialog
        self.file = file
