from ecs_pattern import entity

from components import SpriteComponent, TransformComponent


@entity
class TileEntity(SpriteComponent, TransformComponent):
    pass
