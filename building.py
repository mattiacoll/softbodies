from __future__ import annotations
from math import sqrt
from scipy.constants import g
import pygame
from points import Point


class System:
    nodes: list[Node]
    links: list[Link]

    def __init__(self, nodes: list[Node], links: list[Link]) -> None:
        self.nodes = nodes
        self.links = links

    def __str__(self) -> str:
        return f"Nodes {self.nodes}\nLinks {self.links}"

    def iterate(self, delta_time: float) -> None:
        for node in self.nodes:
            node.iterate(delta_time)


class Node:
    mass: float
    position: Point
    velocity: Point
    acceleration: Point
    force: Point

    def __init__(self, mass: float, position: Point, velocity: Point, acceleration: Point, force: Point) -> None:
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.force = force

    def __repr__(self) -> str:
        return f"Node{self.position}"

    def update_acceleration(self) -> None:
        self.acceleration = self.force / self.mass

    def iterate(self, delta_time) -> None:
        self.update_acceleration()
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time


class Link:
    nodes: tuple[Node, Node]
    resting_distance: float
    actual_distance: float
    stiffness: float
    dampening: float
    actual_speed: float

    def __init__(self, nodes: tuple[Node, Node], resting_distance: float, actual_distance: float, stiffness: float, dampening: float, actual_speed: float) -> None:
        self.nodes = nodes
        self.resting_distance = resting_distance
        self.actual_distance = actual_distance
        self.stiffness = stiffness
        self.dampening = dampening
        self.actual_speed = actual_speed

    def __repr__(self) -> str:
        return f"{self.nodes[0].position} <- Link -> {self.nodes[1].position}"

    def get_unit_vector(self) -> Point:
        return (self.nodes[1].position - self.nodes[0].position) / self.resting_distance

    def get_displacement(self) -> float:
        return self.actual_distance - self.resting_distance

    def get_stiffness_force(self) -> float:
        return -self.stiffness * self.get_displacement()

    def get_dampening_force(self) -> float:
        return -self.dampening * self.actual_speed

    def get_spring_force(self) -> float:
        return self.get_stiffness_force() + self.get_dampening_force()

    def update_actual_distance(self) -> float:
        previous_distance = self.actual_distance
        self.actual_distance = Point.dist(self.nodes[0].position, self.nodes[1].position)
        return previous_distance

    def update_actual_speed(self, delta_time: float) -> None:
        previous_distance = self.update_actual_distance()
        self.actual_speed = (self.actual_distance - previous_distance) / delta_time

    def apply_forces(self) -> None:
        self.nodes[0].force += self.get_spring_force() * self.get_unit_vector()
        self.nodes[1].force -= self.get_spring_force() * self.get_unit_vector()


length = 10
width = 5
height = 20

nodes = [[[Node(mass=1, position=Point(x, y, z), velocity=Point(0, 0, 0), acceleration=Point(0, 0, 0), force=Point(0, 0, 0))
         for z in range(height + 1)] for y in range(width + 1)] for x in range(length + 1)]
links = []

for x in range(1, length - 1):
    for y in range(1, width):
        for z in range(1, height):
            links.append(Link(nodes=(nodes[x][y][z], nodes[x + 1][y][z]),
                              resting_distance=0.9,
                              actual_distance=1,
                              stiffness=1,
                              dampening=1,
                              actual_speed=0))

system = System(nodes=[nodes[x][y][z] for x in range(length + 1) for y in range(width + 1) for z in range(height + 1)], links=links)


iteration = 1
iterations = 1000
delta_time = 0.01

camera_position = Point(0, 0, 0)
camera_focal_distance = 1


def transformed(position: Point) -> Point:
    try:
        return Point(500 * ((position.x - camera_position.x) * camera_focal_distance / ((position.z - camera_position.z) + 20) + 0.5), 500 * ((position.y - camera_position.y) * camera_focal_distance / ((position.z - camera_position.z) + 20) + 0.5))
    except ZeroDivisionError:
        return Point(0, 0)


pygame.init()
screen = pygame.display.set_mode([500, 500])

running = True

for i in range(iterations):
    camera_position.x += 0.1

    for node in system.nodes:
        node.force.set(Point(0, 0, 0))

    for link in system.links:
        link.update_actual_speed(delta_time)
        link.apply_forces()

    for node in system.nodes:
        node.iterate(delta_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    screen.fill((255, 255, 255))

    for link in system.links:
        t1 = transformed(link.nodes[0].position)
        t2 = transformed(link.nodes[1].position)
        pygame.draw.line(screen, (255, 0, 0), (t1.x, t1.y), (t2.x, t2.y), 3)

    for node in system.nodes:
        t1 = transformed(node.position)
        pygame.draw.circle(screen, (0, 0, 255), (t1.x, t1.y), 3)

    pygame.display.flip()
    iteration += 1