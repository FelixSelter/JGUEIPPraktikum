from abc import abstractmethod
from typing import List

from ecs_pattern import component, System, EntityManager

from components.transform_component import TransformComponent
from resources import CameraResource, TimeResource


class Attack:
    last_attack_time: float = 0

    def __init__(self, attack_delay: float):
        self.attack_delay = attack_delay

    @abstractmethod
    def execute_attack(self, entities: EntityManager):
        pass


@component
class AttackComponent:
    """
    Requires TransformComponent
    """
    attacks: List[Attack]


class AttackSystem(System):

    def __init__(self, entities: EntityManager):
        self.entities = entities

    def update(self):
        camera_rsc: CameraResource = next(self.entities.get_by_class(CameraResource))
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))

        for entity in self.entities.get_with_component(AttackComponent, TransformComponent):
            attack_comp: AttackComponent = entity
            transform: TransformComponent = entity

            # Only attack if on screen
            visible_x = camera_rsc.x < transform.position.x + transform.width or transform.position.x + transform.width < camera_rsc.x + camera_rsc.screenWidthInTiles
            visible_y = camera_rsc.y < transform.position.y + transform.height or transform.position.y + transform.height < camera_rsc.y + camera_rsc.screenHeightInTiles
            if visible_x and visible_y:

                # Execute all available attacks and reset their delay
                for attack in attack_comp.attacks:
                    if attack.last_attack_time + attack.attack_delay < time_rsc.totalTime:
                        attack.last_attack_time = time_rsc.totalTime
                        attack.execute_attack(self.entities)
