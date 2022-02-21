"""Python module for dealing with two-dimensional cartesian coordinates and vector operations."""

from __future__ import annotations
from math import cos, hypot, sin
from collections.abc import Iterator


class Point:
    """Two-dimensional point represented in cartesian coordinates."""
    x: float
    y: float

    def __init__(self, x: float, y: float) -> None:
        """Instantiate a point from cartesian coordinates."""
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[float]:
        """Iterate through the pair of coordinates."""
        yield self.x
        yield self.y

    def __add__(self, point: Point, /) -> Point:
        """(+) Add caller point with parameter point, without modification to point."""
        return self.copy().add(point)

    def __iadd__(self, point: Point, /) -> Point:
        """(+=) Add caller point with parameter point, with modification to caller point."""
        return self.add(point)

    def __sub__(self, point: Point, /) -> Point:
        """(-) Subtract parameter point from caller point, without modification to point."""
        return self.copy().sub(point)

    def __isub__(self, point: Point, /) -> Point:
        """(-=) Subtract parameter point from caller point, with modification to caller point."""
        return self.sub(point)

    def __mul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to point."""
        return self.copy().mul(multiplier)

    def __rmul__(self, multiplier: float, /) -> Point:
        """(*) Multiply point coordinates by a number, without modification to point."""
        return self.copy().mul(multiplier)

    def __imul__(self, multiplier: float, /) -> Point:
        """(*=) Multiply point coordinates by a number, with modification to point."""
        return self.mul(multiplier)

    def __truediv__(self, divisor: float, /) -> Point:
        """(/) Divide point coordinates by a number, without modification to point."""
        return self.copy().div(divisor)

    def __itruediv__(self, divisor: float, /) -> Point:
        """(/=) Divide point coordinates by a number, with modification to point."""
        return self.div(divisor)

    def __pos__(self) -> Point:
        """(+) Return the same point instance."""
        return self

    def __neg__(self) -> Point:
        """(-) Flip the sign of point coordinates, without modification to point."""
        return self.copy().mul(-1)

    def __matmul__(self, point: Point, /) -> float:
        """(@) Find the dot product of two points as vectors."""
        return self.dot(point)

    def __mod__(self, point: Point, /) -> float:
        """(%) Find the cross product of two points as vectors."""
        return self.cross(point)

    def set(self, point: Point, /) -> Point:
        """Set coordinates of caller point to match parameter point."""
        self.x = point.x
        self.y = point.y
        return self

    def add(self, point: Point, /) -> Point:
        """Add caller point with parameter point, with modification to caller point."""
        self.x += point.x
        self.y += point.y
        return self

    def sub(self, point: Point, /) -> Point:
        """Subtract parameter point from caller point, with modification to caller point."""
        self.x -= point.x
        self.y -= point.y
        return self

    def mul(self, multiplier: float, /) -> Point:
        """Multiply point coordinates by a number, with modification to point."""
        self.x *= multiplier
        self.y *= multiplier
        return self

    def div(self, divisor: float, /) -> Point:
        """Divide point coordinates by a number, with modification to point."""
        self.x /= divisor
        self.y /= divisor
        return self

    def len(self) -> float:
        """Find the distance to the origin."""
        return hypot(self.x, self.y)

    def dist(self, point: Point, /) -> float:
        """Find the distance between two points."""
        return hypot(self.x - point.x, self.y - point.y)

    def dot(self, point: Point, /) -> float:
        """Find the dot product of two points."""
        return self.x * point.x + self.y * point.y

    def cross(self, point: Point, /) -> float:
        """Find the cross product of two points."""
        return self.x * point.y - self.y * point.x

    def copy(self) -> Point:
        """Copy the point instance."""
        return Point(self.x, self.y)
