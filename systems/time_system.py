import time

from ecs_pattern import System, EntityManager

from resources import TimeResource


class TimeSystem(System):

    def __init__(self, entities: EntityManager):
        self.entities = entities
        self.last_time = time.time()

    def update(self):
        time_rsc: TimeResource = next(self.entities.get_by_class(TimeResource))
        if not time_rsc.paused:
            t = time.time()
            time_rsc.deltaTime = t - self.last_time
            time_rsc.totalTime += time_rsc.deltaTime
            self.last_time = t
        elif time_rsc.doUnPause:
            self.last_time = time.time()
            time_rsc.paused = False
            time_rsc.doUnPause = False
