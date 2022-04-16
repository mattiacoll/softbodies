from __future__ import annotations
from math import cos, sin, tau, sqrt
from random import random
from softbodies import Node, Link, Point

softbody = tuple[list[Node], list[Link]]


def tower(position: Point, size: tuple[float, float], grid: tuple[int, int], mass: float, stiffness: float, dampening: float) -> softbody:
    nodes_mesh = []
    for x in range(grid[0] + 1):
        nodes_mesh.append([])
        for y in range(grid[1] + 1):
            node_mass = mass / ((grid[0] + 1) * (grid[1] + 1))
            node_position = Point(position.x + size[0] * (x / grid[0] - 0.5),
                                  position.y + size[1] * (y / grid[1] - 0.5))
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
    return nodes, links


def pyramid(position: Point, size: tuple[float, float], grid: int, mass: float, stiffness: float, dampening: float) -> softbody:
    nodes_mesh = []
    for y in range(grid + 1):
        nodes_mesh.append([])
        for x in range(grid + 1 - y):
            node_mass = mass / ((grid + 1) * (grid + 2) / 2)
            node_position = Point(position.x - size[0] / 2 + x, position.y - size[1] / 2 + y)
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
    return nodes, links


def blob(position: Point, size: float) -> softbody:
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
    return nodes, links
