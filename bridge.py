from __future__ import annotations
from math import sqrt
import numpy as np
from scipy.constants import g
import pygame
from vectors import Vector


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
    position: Vector
    velocity: Vector
    acceleration: Vector
    force: Vector

    def __init__(self, mass: float, position: Vector, velocity: Vector, acceleration: Vector, force: Vector) -> None:
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

    def get_unit_vector(self) -> Vector:
        return (self.nodes[0].position - self.nodes[1].position) / self.resting_distance

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
        self.actual_distance = Vector.dist(self.nodes[0].position, self.nodes[1].position)
        return previous_distance

    def update_actual_speed(self, delta_time: float) -> None:
        previous_distance = self.update_actual_distance()
        self.actual_speed = (self.actual_distance - previous_distance) / delta_time

    def apply_forces(self) -> None:
        self.nodes[0].force += self.get_spring_force() * self.get_unit_vector()
        self.nodes[1].force -= self.get_spring_force() * self.get_unit_vector()


nodes = [Node(mass=10, position=Vector(0, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(1, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(2, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(3, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(4, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(5, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(6, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(7, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(8, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(9, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(10, 0), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),

         Node(mass=10, position=Vector(0, -2), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0)),
         Node(mass=10, position=Vector(10, -2), velocity=Vector(0, 0), acceleration=Vector(0, 0), force=Vector(0, 0))]

links = [Link(nodes=(nodes[0], nodes[1]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[1], nodes[2]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[2], nodes[3]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[3], nodes[4]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[4], nodes[5]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[5], nodes[6]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[6], nodes[7]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[7], nodes[8]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[8], nodes[9]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[9], nodes[10]), resting_distance=1, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),

         Link(nodes=(nodes[11], nodes[3]), resting_distance=4, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1),
         Link(nodes=(nodes[12], nodes[7]), resting_distance=4, actual_distance=1, stiffness=2000, dampening=100, actual_speed=1)]

system = System(nodes=nodes, links=links)


iteration = 1
iterations = 30000
delta_time = 0.001



view_minimum = Vector(-2, -6)
view_maximum = Vector(12, 8)

pygame.init()
screen = pygame.display.set_mode([500, 500])

def transformed(point: Vector) -> Vector:
    return Vector(500 * (point.x - view_minimum.x) / (view_maximum.x - view_minimum.x),
                  500 * (1 - (point.y - view_minimum.y) / (view_maximum.y - view_minimum.y)))

running = True

for i in range(iterations):
    for node in system.nodes:
        node.force.set(Vector(0, 0, 0))

    for node in system.nodes:
        node.force.y -= node.mass * g

    for link in system.links:
        link.update_actual_speed(delta_time)
        link.apply_forces()

    for node in system.nodes:
        node.iterate(delta_time)

    system.nodes[0].position.set(Vector(0, 0))
    system.nodes[10].position.set(Vector(10, 0))
    system.nodes[11].position.set(Vector(0, -2))
    system.nodes[12].position.set(Vector(10, -2))

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

pygame.quit()