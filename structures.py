from __future__ import annotations
from math import sqrt, cos, sin, atan2, tau
from random import random
from typing import NewType
from softbodies import Node, Link
from vectors import Vector

Softbody = tuple[list[Node], list[Link]]


def structure(softbody: Softbody, position: Vector, scale: float, rotation: float) -> Softbody:
    nodes, links = softbody
    for node in nodes:
        node_angle = atan2(node.position.y, node.position.x)
        node_radius = node.position.dist(Vector(0, 0))
        node.position.x = node_radius * cos(node_angle + rotation)
        node.position.y = node_radius * sin(node_angle + rotation)
        node.position *= scale
        node.position += position
    return nodes, links


def tower(position: Vector, size: tuple[float, float], grid: tuple[int, int], mass: float, stiffness: float, dampening: float) -> Softbody:
    nodes_mesh = []
    for x in range(grid[0] + 1):
        nodes_mesh.append([])
        for y in range(grid[1] + 1):
            node_mass = mass / ((grid[0] + 1) * (grid[1] + 1))
            node_position = Vector(size[0] * (x / grid[0] - 0.5),
                                   size[1] * (y / grid[1] - 0.5))
            nodes_mesh[x].append(Node(node_mass, node_position))
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
    for x in range(grid[0]):
        for y in range(grid[1]):
            links.append(Link((nodes_mesh[x + 1][y], nodes_mesh[x][y + 1]), stiffness, dampening))
    nodes = [node for buffer in nodes_mesh for node in buffer]
    return structure((nodes, links), position, 1, 0)


def pyramid(position: Vector, size: tuple[float, float], grid: int, mass: float, stiffness: float, dampening: float) -> Softbody:
    nodes_mesh = []
    for y in range(grid + 1):
        nodes_mesh.append([])
        for x in range(grid + 1 - y):
            node_mass = mass / ((grid + 1) * (grid + 2) / 2)
            node_position = Vector(-size[0] / 2 + x, -size[1] / 2 + y)
            nodes_mesh[y].append(Node(node_mass, node_position))
    links = []
    for y in range(grid + 1):
        for x in range(grid - y):
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y][x + 1]), stiffness, dampening))
    for y in range(grid):
        for x in range(grid - y):
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y + 1][x]), stiffness, dampening))
    for y in range(grid):
        for x in range(grid - y):
            links.append(Link((nodes_mesh[y][x + 1], nodes_mesh[y + 1][x]), stiffness, dampening))
    nodes = [node for buffer in nodes_mesh for node in buffer]
    return structure((nodes, links), position, rotation=0, scale=1)


def blob(position: Vector, size: float) -> Softbody:
    nodes = []
    for n in range(30):
        radius = (size / 2) * sqrt(random())
        angle = tau * random()
        nodes.append(Node(mass=1, position=Vector(position.x + radius * cos(angle), position.y + radius * sin(angle))))
    links = []
    for n1 in range(30):
        for n2 in range(n1 + 1, 30):
            node_1 = nodes[n1]
            node_2 = nodes[n2]

            if Vector.dist(node_1.position, node_2.position) <= size / 5:
                links.append(Link(nodes=(node_1, node_2), stiffness=200, dampening=0))
    return structure((nodes, links), position, rotation=0, scale=1)
