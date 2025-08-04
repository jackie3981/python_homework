# Task 5

import math

# Base class: Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        if not isinstance(other, Point):
            raise ValueError("distance_to() expects a Point or subclass")
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

# Subclass: Vector
class Vector(Point):
    def __str__(self):
        return f"Vector⟨{self.x}, {self.y}⟩"

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

# -----------------------
# Examples:
if __name__ == "__main__":
    p1 = Point(2, 3)
    p2 = Point(2, 3)
    p3 = Point(5, 7)

    print(p1)                  # Point(2, 3)
    print(p1 == p2)            # True
    print(p1 == p3)            # False
    print(p1.distance_to(p3))  # Euclidian distance

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    v3 = v1 + v2               # Vector addition

    print(v1)                  # Vector⟨1, 2⟩
    print(v2)                  # Vector⟨3, 4⟩
    print(v3)                  # Vector⟨4, 6⟩
