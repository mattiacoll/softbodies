from __future__ import annotations
from math import sqrt, cos, sin, atan2, tau
from random import random
from softbodies import Node, Link
from vectors import Vector

Softbody = tuple[list[Node], list[Link]]


def translate(softbody: Softbody, translation: Vector) -> None:
    nodes, links = softbody
    for node in nodes:
        node.position += translation


def scale(softbody: Softbody, factor: float, center: Vector = None) -> None:
    nodes, links = softbody
    if center is None:
        center = Vector(0, 0)
    translate(softbody, -center)
    for node in nodes:
        node.position *= factor
    for link in links:
        link.resting_length *= factor
    translate(softbody, center)


def rotate(softbody: Softbody, rotation: float, center: Vector = None) -> None:
    nodes, links = softbody
    if center is None:
        center = Vector(0, 0)
    translate(softbody, -center)
    for node in nodes:
        node_angle = atan2(node.position.y, node.position.x)
        node_radius = node.position.len()
        node.position.x = node_radius * cos(node_angle + rotation)
        node.position.y = node_radius * sin(node_angle + rotation)
    translate(softbody, center)


def tower(position: Vector, width: float, height: float, grid: tuple[int, int], mass: float, stiffness: float, dampening: float) -> Softbody:
    nodes_mesh = []
    for x in range(grid[0] + 1):
        nodes_mesh.append([])
        for y in range(grid[1] + 1):
            node_mass = mass / ((grid[0] + 1) * (grid[1] + 1))
            node_position = Vector(position.x + width * (x / grid[0] - 0.5),
                                   position.y + height * (y / grid[1] - 0.5))
            node = Node(node_mass, node_position)
            nodes_mesh[x].append(node)
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
    return softbody


def pyramid(position: Vector, width: float, grid: int, mass: float, stiffness: float, dampening: float) -> Softbody:
    height = (sqrt(3) / 2) * width
    nodes_mesh = []
    for y in range(grid + 1):
        nodes_mesh.append([])
        for x in range(grid + 1 - y):
            node_mass = mass / ((grid + 1) * (grid + 2) / 2)
            node_position = Vector(position.x + width * ((x + 0.5 * y) / grid - 0.5),
                                   position.y + height * (y / grid - 0.5))
            node = Node(node_mass, node_position)
            nodes_mesh[y].append(node)
    links = []
    for y in range(grid):
        for x in range(grid - y):
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y + 1][x]), stiffness, dampening))
            links.append(Link((nodes_mesh[y][x], nodes_mesh[y][x + 1]), stiffness, dampening))
            links.append(Link((nodes_mesh[y][-x - 1], nodes_mesh[y + 1][-x - 1]), stiffness, dampening))
    nodes = [node for buffer in nodes_mesh for node in buffer]
    softbody = (nodes, links)
    return softbody


def wheel(position: Vector, radius: float, rings: int, slices: int, mass: float, stiffness: float, dampening: float) -> Softbody:
    node_mass = mass / (rings * slices + 1)
    nodes_mesh = [[Node(node_mass, position.copy())]]
    for r in range(1, rings + 1):
        nodes_mesh.append([])
        for s in range(slices):
            ang = (s / slices) * tau
            rad = (r / rings) * radius
            node_position = Vector(position.x + rad * cos(ang),
                                   position.y + rad * sin(ang))
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
    softbody = (nodes, links)
    return softbody