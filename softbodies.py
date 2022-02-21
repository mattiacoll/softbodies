from __future__ import annotations
from points import Point


class Softbody:
    nodes: list[Node]
    links: list[Link]


class Node:
    mass: float
    position: Point
    velocity: Point
    force: Point

    def __init__(self, mass: float) -> None:
        self.mass = mass

    def iterate(self, time: float):
        self.velocity += self.force * (time / self.mass)
        self.position += self.velocity * time

class Link:
    node_1: Node
    node_2: Node
    distance: float

    def __init__(self, node_1: Node, node_2: Node, distance: float = None) -> None:
        self.node_1 = node_1
        self.node_2 = node_2
        if distance is None:
            self.distance = node_1.position.dist(node_2.position)
        else:
            self.distance = distance