from math import nan, isnan, isqrt
from time import sleep
from scipy.constants import g
import pygame
from vectors import Vector

cloth_nodes: int = 25
nodes_references: list[list[int]] = [[y * isqrt(cloth_nodes) + x for x in range(isqrt(cloth_nodes))] for y in range(isqrt(cloth_nodes))]

nodes: int = cloth_nodes
nodes_mass: list[float] = [1 for n in range(cloth_nodes)]
nodes_position: list[Vector] = [Vector(x, y) for y in range(isqrt(cloth_nodes)) for x in range(isqrt(cloth_nodes))]
nodes_velocity: list[Vector] = [Vector(0, 0) for n in range(cloth_nodes)]
nodes_acceleration: list[Vector] = [Vector(0, 0) for n in range(cloth_nodes)]
nodes_force: list[Vector] = [Vector(0, 0) for n in range(cloth_nodes)]

links: int = 2 * (isqrt(cloth_nodes) * (isqrt(cloth_nodes) - 1) + (isqrt(cloth_nodes) - 1) ** 2)
links_nodes: list[tuple[int, int]] = []
links_resting: list[float] = []
links_distance: list[float] = []
links_stiffness: list[float] = []
links_dampening: list[float] = []
links_speed: list[float] = []

# Adding horizontal springs
for y in range(isqrt(cloth_nodes)):
    for x in range(isqrt(cloth_nodes) - 1):
        links_nodes.append((nodes_references[y][x], nodes_references[y][x + 1]))
        links_resting.append(0.9)
        links_distance.append(1)
        links_stiffness.append(200)
        links_dampening.append(5)
        links_speed.append(0)

# Adding vertical springs
for x in range(isqrt(cloth_nodes)):
    for y in range(isqrt(cloth_nodes) - 1):
        links_nodes.append((nodes_references[y][x], nodes_references[y + 1][x]))
        links_resting.append(0.9)
        links_distance.append(1)
        links_stiffness.append(200)
        links_dampening.append(5)
        links_speed.append(0)

# Adding diagonal springs
for x in range(isqrt(cloth_nodes) - 1):
    for y in range(isqrt(cloth_nodes) - 1):
        links_nodes.append((nodes_references[x][y], nodes_references[x + 1][y + 1]))
        links_resting.append(1.3)
        links_distance.append(1)
        links_stiffness.append(200)
        links_dampening.append(5)
        links_speed.append(0)
for x in range(isqrt(cloth_nodes) - 1):
    for y in range(isqrt(cloth_nodes) - 1):
        links_nodes.append((nodes_references[x][y + 1], nodes_references[x + 1][y]))
        links_resting.append(1.3)
        links_distance.append(1)
        links_stiffness.append(200)
        links_dampening.append(5)
        links_speed.append(0)

iterations: int = 10000
time_step: float = 0.001
view_minimum = Vector(-1, -2)
view_maximum = Vector(6, 5)



pygame.init()
screen = pygame.display.set_mode([500, 500])


def transform(point: Vector) -> Vector:
    return Vector(500 * (point.x - view_minimum.x) / (view_maximum.x - view_minimum.x),
                  500 * (1 - (point.y - view_minimum.y) / (view_maximum.y - view_minimum.y)))

running = True

for i in range(iterations):
    # Clearing forces
    for n in range(nodes):
        nodes_force[n].set(Vector(0, 0))

    # Force of gravity
    for n in range(nodes):
        nodes_force[n].y -= nodes_mass[n] * g

    for l in range(links):
        link_nodes = links_nodes[l]
        link_distance = Vector.dist(nodes_position[link_nodes[0]], nodes_position[link_nodes[1]])

        # Finding speed of expansion/contraction before distance set
        links_speed[l] = (link_distance - links_distance[l]) / time_step
        links_distance[l] = link_distance
        force_stiffness = -links_stiffness[l] * (link_distance - links_resting[l])
        force_dampening = links_dampening[l] * links_speed[l]
        # Force of spring (one-sided)
        force_spring = (force_stiffness - force_dampening) * (nodes_position[link_nodes[0]] - nodes_position[link_nodes[1]]) / link_distance
        nodes_force[link_nodes[0]].add(force_spring)
        nodes_force[link_nodes[1]].sub(force_spring)

    # Integration
    for n in range(nodes):
        if n == 24:
            nodes_force[n].set(Vector(0, 0))


        nodes_acceleration[n] = nodes_force[n] / nodes_mass[n]
        nodes_velocity[n] += nodes_acceleration[n] * time_step
        nodes_position[n] += nodes_velocity[n] * time_step

    # Conditions
    # enter here

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not running:
        break

    screen.fill((255, 255, 255))

    for l in range(links):
        link_nodes = links_nodes[l]
        transformed_1 = transform(nodes_position[link_nodes[0]])
        transformed_2 = transform(nodes_position[link_nodes[1]])
        pygame.draw.line(screen, (255, 0, 0), (transformed_1.x, transformed_1.y), (transformed_2.x, transformed_2.y), 3)

    for n in range(nodes):
        transformed = transform(nodes_position[n])
        pygame.draw.circle(screen, (0, 0, 255), (transformed.x, transformed.y), 5)

    pygame.display.flip()

pygame.quit()
