from __future__ import annotations
from math import sqrt, cos, sin, atan2, tau
from random import random
from softbodies import Node, Link
from vectors import Vector

Softbody = tuple[list[Node], list[Link]]


class Structure:
    nodes: list[Node]
    links: list[Link]

    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        self.nodes = nodes
        self.links = links

    def translate(self, translation: Vector) -> None:
        for node in self.nodes:
            node.position += translation

    def scale(self, factor: Vector) -> None:
        for node in self.nodes:
            node.position.x *= factor.x
            node.position.y *= factor.y

    def rotate(self, radians: float) -> None:
        for node in self.nodes:
            node_angle = atan2(node.position.y, node.position.x)
            node_radius = node.position.dist(Vector(0, 0))
            node.position.x = node_radius * cos(node_angle + radians)
            node.position.y = node_radius * sin(node_angle + radians)


class Tower(Structure):
    nodes_mesh: list[list[Node]]

    def __init__(self, position: Vector, width: float, height: float, grid: tuple[int, int], mass: float, stiffness: float, dampening: float) -> None:
        nodes_mesh = []
        for x in range(grid[0] + 1):
            nodes_mesh.append([])
            for y in range(grid[1] + 1):
                node_mass = mass / ((grid[0] + 1) * (grid[1] + 1))
                node_position = Vector(x / grid[0], y / grid[1])
                node = Node(node_mass, node_position)
                nodes_mesh[x].append(node)
        self.nodes_mesh = nodes_mesh
        links = []
        for x in range(grid[0]):
            for y in range(grid[1] + 1):
                links.append(Link((nodes_mesh[x][y], nodes_mesh[x + 1][y]), stiffness, dampening))
        for x in range(grid[0] + 1):
            for y in range(grid[1]):
                links.append(Link((nodes_mesh[x][y], nodes_mesh[x][y + 1]), stiffness, dampening))
        for x in range(grid[0]):
            for y in range(grid[1]):
                links.append(Link((nodes_mesh[x][y], nodes_mesh[x + 1][y + 1]), stiffness, dampening))
                links.append(Link((nodes_mesh[x + 1][y], nodes_mesh[x][y + 1]), stiffness, dampening))
        nodes = [node for buffer in nodes_mesh for node in buffer]
        super().__init__(nodes, links)
        self.translate(Vector(-0.5, -0.5))
        self.scale(Vector(width, height))
        self.translate(position)


class Pyramid(Structure):
    def __init__(self, position: Vector, width: float, grid: int, mass: float, stiffness: float, dampening: float) -> None:
        height = (sqrt(3) / 2) * width
        nodes_mesh = []
        for y in range(grid + 1):
            nodes_mesh.append([])
            for x in range(grid + 1 - y):
                node_mass = mass / ((grid + 1) * (grid + 2) / 2)
                node_position = Vector((x + 0.5 * y) / grid, y / grid)
                node = Node(node_mass, node_position)
                nodes_mesh[y].append(node)
        links = []
        for y in range(grid):
            for x in range(grid - y):
                links.append(Link((nodes_mesh[y][x], nodes_mesh[y + 1][x]), stiffness, dampening))
                links.append(Link((nodes_mesh[y][x], nodes_mesh[y][x + 1]), stiffness, dampening))
                links.append(Link((nodes_mesh[y][-x - 1], nodes_mesh[y + 1][-x - 1]), stiffness, dampening))
        nodes = [node for buffer in nodes_mesh for node in buffer]
        super().__init__(nodes, links)
        self.translate(Vector(-0.5, -0.5))
        self.scale(Vector(width, height))
        self.translate(position)


class Wheel(Structure):
    def __init__(self, position: Vector, radius: float, rings: int, slices: int, mass: float, stiffness: float, dampening: float) -> None:
        node_mass = mass / (rings * slices + 1)
        nodes_mesh = [[Node(node_mass, position.copy())]]
        for r in range(1, rings + 1):
            nodes_mesh.append([])
            for s in range(slices):
                ang = (s / slices) * tau
                rad = (r / rings) * radius
                node_position = Vector(rad * cos(ang), rad * sin(ang))
                node = Node(node_mass, node_position)
                nodes_mesh[r].append(node)
        links = []
        for r in range(1, rings + 1):
            for s in range(slices):
                links.append(Link((nodes_mesh[r][s], nodes_mesh[r][(s + 1) % slices]), stiffness, dampening))
        for s in range(slices):
            links.append(Link((nodes_mesh[0][0], nodes_mesh[1][s]), stiffness, dampening))
        for r in range(1, rings):
            for s in range(slices):
                links.append(Link((nodes_mesh[r][s], nodes_mesh[r + 1][s]), stiffness, dampening))
        nodes = [node for buffer in nodes_mesh for node in buffer]
        super().__init__(nodes, links)
        self.translate(position)