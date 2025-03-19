from ecs_pattern import entity

from Components import SpriteComponent, TransformComponent


@entity
class TileEntity(SpriteComponent, TransformComponent):
    pass
