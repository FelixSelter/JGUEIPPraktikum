from enum import Enum


class CollisionDirection(Enum):
    Top = 0
    Bottom = 1
    Right = 2
    Left = 3

    def mirror(self):
        match self:
            case CollisionDirection.Top:
                return CollisionDirection.Bottom
            case CollisionDirection.Bottom:
                return CollisionDirection.Top
            case CollisionDirection.Left:
                return CollisionDirection.Right
            case CollisionDirection.Right:
                return CollisionDirection.Left
