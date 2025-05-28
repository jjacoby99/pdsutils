from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Iterator

@dataclass(slots=True, frozen=True)
class Vector6:
    x: float; y: float; z: float
    rx: float; ry: float; rz: float      # rotations or moments

    def __add__(self, other: "Vector6") -> "Vector6":
        return Vector6(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other: "Vector6") -> "Vector6":
        return Vector6(*(a - b for a, b in zip(self, other)))

    def __mul__(self, k: float) -> Vector6:          # scalar multiply
        return Vector6(*(a * k for a in self))

    __rmul__ = __mul__

    def dot(self, other: "Vector6") -> float:
        return sum(a * b for a, b in zip(self, other))

    def norm(self) -> float:
        return sqrt(sum(a*a for a in self))

    # iterable support lets you treat it like a tuple
    def __iter__(self):
        yield from (self.x, self.y, self.z, self.rx, self.ry, self.rz)

    @classmethod
    def from_iter(cls, data: Iterable[float]) -> "Vector6":
        data = tuple(data)
        if len(data) != 6:
            raise ValueError(f"Vector6 needs exactly 6 elements")
        return cls(*map(float, data))

    def to_tuple(self) -> tuple[float, ...]:
        return tuple(self)


