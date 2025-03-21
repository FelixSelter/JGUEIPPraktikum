from math import floor, copysign


class Vec2:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __iadd__(self, other):
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y
            return self
        else:
            raise ValueError("Can only add Vec+Vec")

    def __mul__(self, other):
        if isinstance(other, float):
            return Vec2(self.x * other, self.y * other)
        else:
            raise ValueError("Can only multiply Vec*float")

    def __repr__(self):
        return f"Vec2({self.x}|{self.y})"


def fract(f):
    return f - floor(f)


def sign_zero(f):
    return 0 if f == 0 else copysign(1, f)
