from __future__ import annotations
from points import Point


class Softbody:
    nodes: list[Node]
    links: list[Link]

    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        self.nodes = nodes
        self.links = links


class Node:
    mass: float
    position: Point
    velocity: Point
    acceleration: Point
    force: Point

    def __init__(self, mass: float, position: Point) -> None:
        self.mass = mass
        self.position = position

    def apply_force(self, force: Point) -> None:
        self.force += force


class Link:
    nodes: tuple[Node, Node]
    resting_length: float
    stiffness: float
    dampening: float

    def __init__(self, nodes: tuple[Node, Node], resting_length: float, stiffness: float, dampening: float) -> None:
        self.nodes = nodes
        self.resting_length = resting_length
        self.stiffness = stiffness
        self.dampening = dampening

    def get_length(self) -> float:
        return Point.dist(self.nodes[0].position, self.nodes[1].position)

    def get_speed(self) -> float:
        return Point.dot(self.nodes[0].position - self.nodes[1].position, self.nodes[0].velocity - self.nodes[1].velocity) / self.get_length()

    def get_displacement(self) -> float:
        return self.get_length() - self.resting_length

    def get_stiffness_force(self) -> float:
        return -self.stiffness * self.get_displacement()

    def get_dampening_force(self) -> float:
        return -self.dampening * self.get_speed()

    def get_force(self) -> float:
        return self.get_stiffness_force() + self.get_dampening_force()

    def apply_force(self) -> None:
        self.nodes[0].apply_force(self.get_spring_force() * ((self.nodes[0].position - self.nodes[1].position) / self.get_length()))
        self.nodes[1].apply_force(self.get_spring_force() * ((self.nodes[1].position - self.nodes[0].position) / self.get_length()))

