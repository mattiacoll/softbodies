from itertools import combinations
from math import cos, sin, tau
from softbodies import Softbody, Node, Link, Point


class HollowPolygon(Softbody):
    def __init__(self, center: Point, major_radius: float, total_mass: float, number_sides: int, stiffness: float, dampening: float) -> None:
        nodes = []
        for n in range(number_sides):
            angle = tau * (n / number_sides)
            offset = Point(major_radius * cos(angle), major_radius * sin(angle))
            nodes.append(Node(mass=total_mass / number_sides,
                              position=center + offset))

        links = []
        for n in range(number_sides):
            links.append(Link(nodes=(nodes[n], nodes[(n + 1) % number_sides]),
                              stiffness=stiffness,
                              dampening=dampening))
        super().__init__(nodes, links)


class CrazyPolygon(Softbody):
    def __init__(self, center: Point, major_radius: float, total_mass: float, number_sides: int, stiffness: float, dampening: float):
        nodes = []
        for n in range(number_sides):
            angle = tau * (n / number_sides)
            offset = Point(major_radius * cos(angle), major_radius * sin(angle))
            nodes.append(Node(mass=total_mass / number_sides,
                              position=center + offset))

        links = []
        for pair_nodes in combinations(nodes, 2):
            links.append(Link(nodes=pair_nodes,
                              stiffness=stiffness,
                              dampening=dampening))
        super().__init__(nodes, links)


a = CrazyPolygon(center=Point(0, 0), major_radius=1, total_mass=100, number_sides=10, stiffness=25, dampening=1)