from __future__ import annotations
from points import Point


class Softbody:
    """A spring-network type softbody consisting of nodes (point masses) and links (Hookean springs)."""
    nodes: list[Node]
    links: list[Link]

    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        self.nodes = nodes
        self.links = links

    def get_total_mass(self) -> float:
        total_mass = 0
        for node in self.nodes:
            total_mass += node.mass
        return total_mass

    def get_center_mass(self) -> Point:
        center_mass = Point(0, 0)
        for node in self.nodes:
            center_mass += node.mass * node.position
        return center_mass

    def iterate(self, time) -> None:
        """Integrate the position and velocity of each node with Euler's method."""
        for node in self.nodes:
            node.iterate(time)


class Node:
    """A point mass particle that implements Euler integration."""
    mass: float
    position: Point
    velocity: Point
    force: Point

    def __init__(self, mass: float, position: Point) -> None:
        self.mass = mass
        self.position = position
        self.velocity = Point(0, 0)
        self.force = Point(0, 0)

    def iterate(self, time: float) -> None:
        """Integrate the position and velocity with Euler's method."""
        self.velocity += (self.force / self.mass) * time
        self.position += self.velocity * time


class Link:
    """A massless Hookean spring that features a stiffness force and a spring force."""
    nodes: tuple[Node, Node]
    resting_length: float
    stiffness: float
    dampening: float

    def __init__(self, nodes: tuple[Node, Node], stiffness: float, dampening: float, resting_length: float = None) -> None:
        self.nodes = nodes
        if resting_length is None:
            self.resting_length = Point.dist(nodes[0].position, nodes[1].position)
        else:
            self.resting_length = resting_length
        self.stiffness = stiffness
        self.dampening = dampening

    def get_length(self) -> float:
        """Get the momentary length of the link."""
        return Point.dist(self.nodes[0].position, self.nodes[1].position)

    def get_speed(self) -> float:
        """Get the speed of the expansion/contraction of the link (positive/negative)."""
        return Point.dot(self.nodes[0].position - self.nodes[1].position, self.nodes[0].velocity - self.nodes[1].velocity) / self.get_length()

    def get_displacement(self) -> float:
        """Get the expansion/contraction of the link from its resting configuration (positive/negative)."""
        return self.get_length() - self.resting_length

    def get_stiffness_force(self) -> float:
        """Get the spring stiffness force expansion/contraction (positive/negative)."""
        return -self.stiffness * self.get_displacement()

    def get_dampening_force(self) -> float:
        """Get the spring dampening force expansion/contraction (positive/negative)."""
        return -self.dampening * self.get_speed()

    def get_force(self) -> float:
        """Get the spring force expansion/contraction (positive/negative)."""
        return self.get_stiffness_force() + self.get_dampening_force()

    def iterate(self, time: float) -> None:
        self.nodes[0].iterate(time)
        self.nodes[1].iterate(time)
