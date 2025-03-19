from ecs_pattern import entity

from components.sprite_component import SpriteComponent
from components.transform_component import TransformComponent


@entity
class TileEntity(SpriteComponent, TransformComponent):
    pass
