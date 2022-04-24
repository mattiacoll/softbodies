from vectors import Vector
from structures import tower
from render import render

softbody = tower(position=Vector(0, 0), width=1, height=1, grid=(5, 5), mass=1, stiffness=100, dampening=1)
nodes, links = softbody

for i in range(100):
    for s in range(5):
        for node in nodes:
            node.force.set(Vector(0, -9.80665 * node.mass))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
        nodes[0].force.set(Vector(0, 0))
        for node in nodes:
            node.iterate(time=0.001)

render(softbody, camera_position=Vector(0, 0), camera_zoom=0.5)