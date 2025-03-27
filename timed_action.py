from abc import abstractmethod
from typing import List, Any

from ecs_pattern import component, System, EntityManager

from components.transform_component import TransformComponent
from resources import CameraResource, TimeResource


class TimedAction:
    last_attack_time: float = -1000

    def __init__(self, attack_delay: float, executed_immediate: bool):
        self.attack_delay = attack_delay
        self.executed_immediate = executed_immediate

    def internal_execute_action(self, this: Any, entities: EntityManager):
        if not self.executed_immediate:
            self.executed_immediate = True
            return
        self.execute_action(this, entities)

    @abstractmethod
    def execute_action(self, this: Any, entities: EntityManager):
        pass


@component
class TimedActionComponent:
    """
    Requires TransformComponent
    """
    actions: List[TimedAction]


class TimedActionSystem(System):

    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        camera_rsc: CameraResource = next(self.entities.get_by_class(CameraResource))
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for entity in self.entities.get_with_component(TimedActionComponent, TransformComponent):
            action_comp: TimedActionComponent = entity
            transform: TransformComponent = entity

            # Only attack if on screen
            visible_x = camera_rsc.x < transform.position.x + transform.width or transform.position.x + transform.width < camera_rsc.x + camera_rsc.screenWidthInTiles
            visible_y = camera_rsc.y < transform.position.y + transform.height or transform.position.y + transform.height < camera_rsc.y + camera_rsc.screenHeightInTiles
            if visible_x and visible_y:

                # Execute all available attacks and reset their delay
                for action in action_comp.actions:
                    if action.last_attack_time + action.attack_delay < time_rsc.totalTime:
                        action.last_attack_time = time_rsc.totalTime
                        action.internal_execute_action(entity, self.entities)
