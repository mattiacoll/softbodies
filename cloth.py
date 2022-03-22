from math import nan, isnan
from time import sleep
from scipy.constants import g
import pygame
from points import Point


nodes: int = 4
nodes_mass: list[float] = [1, 1, 1, 1]
nodes_position: list[Point] = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)]
nodes_velocity: list[Point] = [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
nodes_acceleration: list[Point] = [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]
nodes_force: list[Point] = [Point(0, 0), Point(0, 0), Point(0, 0), Point(0, 0)]

links: int = 6
links_nodes: list[tuple[int, int]] = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)]
links_resting: list[float] = [0.9, 0.9, 0.9, 0.9, 1.3, 1.3]
links_distance: list[float] = [nan, nan, nan, nan, nan, nan]
links_stiffness: list[float] = [100, 100, 100, 100, 100, 100]
links_dampening: list[float] = [10, 10, 10, 10, 10, 10]
links_speed: list[float] = [0, 0, 0, 0, 0, 0]

iterations: int = 10000
time_step: float = 0.0001
view_minimum = Point(-1, -1)
view_maximum = Point(2, 2)

pygame.init()
screen = pygame.display.set_mode([1000, 1000])


def transform(point: Point) -> Point:
    return Point(1000 * (point.x - view_minimum.x) / (view_maximum.x - view_minimum.x),
                 1000 * (point.y - view_minimum.y) / (view_maximum.y - view_minimum.y))


for i in range(iterations):
    # Clearing forces
    for n in range(nodes):
        nodes_force[n].set(Point(0, 0))

    # Force of gravity
    for n in range(nodes):
        nodes_force[n].y -= nodes_mass[n] * g

    for l in range(links):
        link_nodes = links_nodes[l]
        link_distance = Point.dist(nodes_position[link_nodes[0]], nodes_position[link_nodes[1]])

        # Finding speed of expansion/contraction before distance set
        if not isnan(links_distance[l]):
            links_speed[l] = (link_distance - links_distance[l]) / time_step
        else:
            links_speed[l] = 0

        links_distance[l] = link_distance

        force_stiffness = -links_stiffness[l] * (link_distance - links_resting[l])
        force_dampening = -links_dampening[l] * links_speed[l]
        # Force of spring (one-sided)
        force_spring = (force_stiffness + force_dampening) * (nodes_position[link_nodes[0]] - nodes_position[link_nodes[1]]) / link_distance
        nodes_force[link_nodes[0]].add(force_spring)
        nodes_force[link_nodes[1]].sub(force_spring)

    # Integration
    for n in range(nodes):
        print(*nodes_force[n])
        nodes_acceleration[n] = nodes_force[n] / nodes_mass[n]
        nodes_velocity[n] += nodes_acceleration[n] * time_step
        nodes_position[n] += nodes_velocity[n] * time_step

    # Conditions
    nodes_position[0].set(Point(0, 0))
    nodes_position[1].set(Point(1, 0))

    screen.fill((255, 255, 255))

    for l in range(links):
        link_nodes = links_nodes[l]
        transformed_1 = transform(nodes_position[link_nodes[0]])
        transformed_2 = transform(nodes_position[link_nodes[1]])
        pygame.draw.line(screen, (0, 0, 255), (transformed_1.x, transformed_1.y), (transformed_2.x, transformed_2.y), 3)

    for n in range(nodes):
        transformed = transform(nodes_position[n])
        pygame.draw.circle(screen, (255, 0, 0), (transformed.x, transformed.y), 10)

    pygame.display.flip()

pygame.quit()