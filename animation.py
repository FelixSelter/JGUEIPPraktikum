from typing import List, Dict

from ecs_pattern import component, System, EntityManager
from pygame import Surface

from components import SpriteComponent
from resources import TimeResource


class AnimationFrame:
    def __init__(self, sprite: Surface, duration: float):
        self.duration = duration
        self.sprite = sprite


class Animation:
    def __init__(self, frames: List[AnimationFrame]):
        self.frames = frames


@component
class AnimationComponent:
    """
    Requires SpriteComponent
    """
    animations: Dict[str, Animation]
    activeAnimation: str
    currentTime: float
    loopAnimation: bool


class AnimationSystem(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for entity in self.entities.get_with_component(SpriteComponent, AnimationComponent):
            sprite: SpriteComponent = entity
            animationHandler: AnimationComponent = entity

            if animationHandler.activeAnimation is None:
                continue

            animationHandler.currentTime += time_rsc.deltaTime
            animation = animationHandler.animations[animationHandler.activeAnimation]

            def findFrame():
                # Find current frame
                time = 0
                for frame in animation.frames:
                    time += frame.duration
                    if time > animationHandler.currentTime:
                        sprite.sprite = frame.sprite
                        break

                # for else executes if there was no break and thus no frame has been found / the animation has completed
                # Restart if loop is active
                else:
                    if animationHandler.loopAnimation and len(animation.frames) > 0:
                        animationHandler.currentTime -= time * (animationHandler.currentTime // time)
                        findFrame()

            findFrame()
