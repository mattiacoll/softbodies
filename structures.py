from __future__ import annotations
from math import sqrt, cos, sin, atan2, tau
from random import random
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


def tower(position: Vector, width: float, height: float, grid: tuple[int, int], mass: float, stiffness: float, dampening: float) -> Softbody:
    nodes_mesh = []
    for x in range(grid[0] + 1):
        nodes_mesh.append([])
        for y in range(grid[1] + 1):
            node_mass = mass / ((grid[0] + 1) * (grid[1] + 1))
            node_position = Vector(position.x + width * (x / grid[0] - 0.5),
                                   position.y + height * (y / grid[1] - 0.5))
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
            links.append(Link((nodes_mesh[x + 1][y], nodes_mesh[x][y + 1]), stiffness, dampening))
    nodes = [node for buffer in nodes_mesh for node in buffer]
    softbody = (nodes, links)
    return structure(softbody, position=Vector(0, 0), scale=1, rotation=0)


def pyramid(position: Vector, width: float, grid: int, mass: float, stiffness: float, dampening: float) -> Softbody:
    height = (sqrt(3) / 2) * width
    nodes_mesh = []
    for y in range(grid + 1):
        nodes_mesh.append([])
        for x in range(grid + 1 - y):
            node_mass = mass / ((grid + 1) * (grid + 2) / 2)
            node_position = Vector(position.x + width * ((x + 0.5 * y) / grid - 0.5),
                                   position.y + height * (y / grid - 0.5))
            nodes_mesh[y].append(Node(node_mass, node_position))
    links = []
    for y in range(grid):
        for x in range(grid - y):
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y + 1][x]), stiffness, dampening))
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y][x + 1]), stiffness, dampening))
            links.append(Link((nodes_mesh[y][-x - 1], nodes_mesh[y + 1][-x - 1]), stiffness, dampening))
    nodes = [node for buffer in nodes_mesh for node in buffer]
    softbody = (nodes, links)
    return structure(softbody, position, rotation=0, scale=1)


