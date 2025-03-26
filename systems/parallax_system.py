import random
import pygame
from pygame.typing import SequenceLike
from abc import ABC, abstractmethod


class Range:
    def __init__(self, min_val: float, max_val: float):
        self.min: float = min_val
        self.max: float = max_val

    def get_random(self) -> float:
        return random.uniform(self.min, self.max)

    def __lt__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self.max < other
        elif isinstance(other, Range):
            return self.max < other.min
        else:
            raise TypeError(f"Can't compare {type(other)} with {type(self)}")

    def __eq__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self.min <= other <= self.max
        elif isinstance(other, Range):
            return self.min == other.min and self.max == other.max
        else:
            raise TypeError(f"Can't compare {type(other)} with {type(self)}")

    def __gt__(self, other) -> bool:
        if isinstance(other, (int, float)):
            return self.min > other
        elif isinstance(other, Range):
            return self.min > other.max
        else:
            raise TypeError(f"Can't compare {type(other)} with {type(self)}")




class ParallaxObject(ABC):
    def __init__(self, z_index: int):
        self.z_index: int = z_index

    @abstractmethod
    def update(self, screen: pygame.Surface, dx, dy): pass



class ParallaxItem(ParallaxObject):
    def __init__(self, x: float, y: float, image: pygame.Surface, scale: SequenceLike[float], z_index: int = 0):
        super().__init__(z_index)
        self.image = pygame.transform.smoothscale(image, scale)

        self.x = x
        self.y = y

    def update(self, screen: pygame.Surface, dx: float, dy: float):
        screen.blit(self.image, (self.x + dx, self.y + dy))



class ParallaxLayer(ParallaxObject):
    def __init__(self, image_path: str, speed: float = 1.0, z_index: int = 0, scale: Range = Range(1, 1), y_offset: float = 0.0):
        super().__init__(z_index)
        self.speed = speed
        self.base_scale: Range = scale

        self.y_offset = y_offset

        # Parallax Object
        self.image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.items: list[ParallaxItem] = []

        self.offset_x = 0.0
        self.offset_y = 0.0

    def add_item(self, x: float, y: float = None, scale: SequenceLike[float] = None) -> SequenceLike[float]:
        if not scale:
            rnd_scale = self.base_scale.get_random()
            scale = (self.image.get_width() * rnd_scale, self.image.get_height() * rnd_scale)

        obj = ParallaxItem(
            x=x,
            y=y if y else self.y_offset,
            image=self.image,
            scale=scale
        )
        self.items.append(obj)
        return scale

    def update(self, screen: pygame.Surface, dx: float, dy: float):
        self.offset_x -= dx * self.speed
        self.offset_y -= dy * self.speed * 0.1

        for item in self.items:
            item.update(screen, self.offset_x, self.offset_y)



class ParallaxManager:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.objects: list[ParallaxObject] = []

    def add_object(self, obj: ParallaxObject):
        self.objects.append(obj)
        self.objects.sort(key=lambda l: l.z_index)

    def update(self, dx: float, dy: float):
        for layer in self.objects:
            layer.update(self.screen, dx, dy)

