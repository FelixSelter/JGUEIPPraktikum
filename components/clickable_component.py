from typing import Callable, Any

from ecs_pattern import component


@component
class ClickableComponent:
    """
    Requires either HitBoxComponent or TileComponent
    """
    click_event_handler: Callable[[Any, (float, float)], None]
