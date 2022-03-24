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

    def get_displacement(self) -> float:
        return self.actual_distance - self.resting_distance

    def get_stiffness_force(self) -> float:
        return -self.stiffness * self.get_displacement()

    def get_dampening_force(self) -> float:
        return -self.dampening * self.actual_speed

    def get_spring_force(self) -> float:
        return self.get_stiffness_force() + self.get_dampening_force()

    def update_actual_distance(self) -> None:
        self.actual_distance = Point.dist(self.nodes[0].position, self.nodes[1].position)

    def update_actual_speed(self, previous_distance: float, delta_time: float) -> None:
        self.actual_speed = (self.actual_distance - previous_distance) / delta_time