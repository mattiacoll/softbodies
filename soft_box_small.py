from math import pi
from vectors import Vector
from structures import Tower
from render import render

tower = Tower(position=Vector(0, 0), width=1, height=1, grid=(3, 3), mass=1, stiffness=20, dampening=1)
tower.rotate(pi / 2)
nodes = tower.nodes
links = tower.links

for i in range(100):
    for s in range(1):
        for node in nodes:
            node.force.set(Vector(0, -9.80665 * node.mass))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))

        for node in tower.nodes_mesh[0]:
            node.force.set(Vector(0, 0))

        for node in nodes:
            node.iterate(time=0.005)

render(nodes, links, camera_position=Vector(0, 0), camera_zoom=0.5)