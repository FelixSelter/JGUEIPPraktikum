from ecs_pattern import entity


@entity
class TimeResource:
    totalTime: float
    deltaTime: float
    doUnPause: bool
    paused: bool


@entity
class CameraResource:
    screenWidthInTiles: int  # number of tiles visible on screen
    screenHeightInTiles: int  # number of tiles visible on screen
    x: float  # In tile coordinates
    y: float  # In tile coordinates
