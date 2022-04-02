from __future__ import annotations
from math import cos, sin, tau, sqrt
from random import random
from softbodies import Softbody, Node, Link, Point


class Structure(Softbody):
    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        super().__init__(nodes, links)




class Tower(Structure):
    def __init__(self, position: Point, size: tuple[float, float], grid: tuple[int, int], mass: float, stiffness: float,
                 dampening: float) -> None:
        nodes = []
        for x in range(grid[0] + 1):
            nodes.append([])
            for y in range(grid[1] + 1):
                nodes[x].append(Node(mass=mass / ((grid[0] + 1) * (grid[1] + 1)),
                                     position=Point(position.x + size[0] * (x / grid[0] - 0.5),
                                                    position.y + size[1] * (y / grid[1] - 0.5))))
        links = []
        for x in range(grid[0]):
            for y in range(grid[1] + 1):
                links.append(Link(nodes=(nodes[x][y], nodes[x + 1][y]), stiffness=stiffness, dampening=dampening))
        for x in range(grid[0] + 1):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x][y], nodes[x][y + 1]), stiffness=stiffness, dampening=dampening))
        for x in range(grid[0]):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x][y], nodes[x + 1][y + 1]), stiffness=stiffness, dampening=dampening))
        for x in range(grid[0]):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x + 1][y], nodes[x][y + 1]), stiffness=stiffness, dampening=dampening))
        super().__init__(nodes=[node for buffer in nodes for node in buffer], links=links)


class Pyramid(Structure):
    def __init__(self, position: Point, size: tuple[float, float], grid: int, mass: float, stiffness: float,
                 dampening: float) -> None:
        nodes = []
        for y in range(grid + 1):
            nodes.append([])
            for x in range(grid + 1 - y):
                nodes[y].append(Node(mass=mass / ((grid + 1) * (grid + 2) / 2),
                                     position=Point(position.x - size[0] / 2 + x,
                                                    position.y - size[1] / 2 + y)))

        links = []
        for y in range(grid + 1):
            for x in range(grid - y):
                links.append(Link(nodes=(nodes[y][x], nodes[y][x + 1]), stiffness=stiffness, dampening=dampening))

        for y in range(grid):
            for x in range(grid - y):
                links.append(Link(nodes=(nodes[y][x], nodes[y + 1][x]), stiffness=stiffness, dampening=dampening))

        for y in range(grid):
            for x in range(grid - y):
                links.append(Link(nodes=(nodes[y][x + 1], nodes[y + 1][x]), stiffness=stiffness, dampening=dampening))

        super().__init__(nodes=[node for buffer in nodes for node in buffer], links=links)


class Blob(Structure):
    def __init__(self, position: Point, size: float) -> None:
        nodes = []
        for n in range(30):
            radius = (size / 2) * sqrt(random())
            angle = tau * random()
            nodes.append(Node(mass=1, position=Point(position.x + radius * cos(angle), position.y + radius * sin(angle))))
        links = []
        for n1 in range(30):
            for n2 in range(n1 + 1, 30):
                node_1 = nodes[n1]
                node_2 = nodes[n2]

                if Point.dist(node_1.position, node_2.position) <= size / 3:
                    links.append(Link(nodes=(node_1, node_2), stiffness=200, dampening=0))

        super().__init__(nodes=nodes, links=links)