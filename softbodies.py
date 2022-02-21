from __future__ import annotations
from points import Point


class Softbody:
    nodes: list[Node]
    links: list[Link]

    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        self.nodes = nodes
        self.links = links

    def iterate(self, time: float) -> None:
        for node in self.nodes:
            node.force = Point(0, -9.88 * node.mass)

        for link in self.links:
            node_1 = link.node_1
            node_2 = link.node_2
            force = Point.polar(10 * (node_1.position.dist(node_2.position) - link.distance), node_1.position.angle(node_2.position))
            node_1.force -= force
            node_2.force += force

        for node in self.nodes:
            node.iterate(time)


class Node:
    mass: float
    position: Point
    velocity: Point
    force: Point

    def __init__(self, mass: float, position: Point, velocity: Point) -> None:
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.force = Point(0, 0)

    def iterate(self, time: float) -> None:
        self.velocity += self.force * (time / self.mass)
        self.position += self.velocity * time


class Link:
    node_1: Node
    node_2: Node
    distance: float

    def __init__(self, node_1: Node, node_2: Node, distance: float = None) -> None:
        self.node_1 = node_1
        self.node_2 = node_2
        if distance is not None:
            self.distance = distance
        else:
            self.distance = node_1.position.dist(node_2.position)