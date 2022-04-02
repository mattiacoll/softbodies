from __future__ import annotations
from softbodies import Softbody, Node, Link, Point


class Tower(Softbody):
    def __init__(self, mass: float, position: Point, size: tuple[float, float], grid: tuple[int, int]) -> None:
        nodes = []
        for x in range(grid[0] + 1):
            nodes.append([])
            for y in range(grid[1] + 1):
                nodes[x].append(Node(mass=mass / ((grid[0] + 1) * (grid[1] + 1)),
                                     position=Point(position.x + size[0] * (x / grid[0]),
                                                    position.y + size[1] * (y / grid[1]))))
        links = []
        for x in range(grid[0]):
            for y in range(grid[1] + 1):
                links.append(Link(nodes=(nodes[x][y], nodes[x + 1][y]), stiffness=5000, dampening=0))
        for x in range(grid[0] + 1):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x][y], nodes[x][y + 1]), stiffness=5000, dampening=0))
        for x in range(grid[0]):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x][y], nodes[x + 1][y + 1]), stiffness=5000, dampening=0))
        for x in range(grid[0]):
            for y in range(grid[1]):
                links.append(Link(nodes=(nodes[x + 1][y], nodes[x][y + 1]), stiffness=5000, dampening=0))
        super().__init__(nodes=[node for buffer in nodes for node in buffer], links=links)