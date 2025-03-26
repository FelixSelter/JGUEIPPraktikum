from ecs_pattern import component
from typing import List

@component
class PlayerComponent:
    speed: float
    maxspeed: float
    jump: float
    key_up: int
    key_right: int
    key_left: int
    key_array: dict[str: bool]
    statusEffects: List[List[float]]
