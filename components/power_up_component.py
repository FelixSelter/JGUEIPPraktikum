from ecs_pattern import component


@component
class PowerUpComponent:
    power: int
    powerDelay: float
