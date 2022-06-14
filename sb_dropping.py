from softbodies import Softbody, Node, Link
from structures import Tower
from vectors import Vector

softbody = Tower(width=0.5, height=0.5, grid=(5, 5), mass=1, stiffness=100, dampening=0)
softbody.translate(Vector(0.5, 0.5))

nodes = softbody.nodes
links = softbody.links

for i in range(1000):
    for node in nodes:
        node.force.set(Vector(0, 0))
    for node in nodes:
        node.force.add(Vector(0, -9.8 * node.mass))
    for link in links:
        node_1 = link.nodes[0]
        node_2 = link.nodes[1]
        node_1_force = link.get_force() * (
                node_1.position - node_2.position
        ) / Vector.dist(node_1.position, node_2.position)
        node_1.force.add(node_1_force)
        node_2.force.sub(node_1_force)
    for node in nodes:
        node_force_normal = Vector(0, 0)
        node_force_friction = Vector(0, 0)
        if node.position.x < 0:
            node_force_normal.add(Vector(-node.position.x, 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.y / abs(node.velocity.y)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.y < 0:
            node_force_normal.add(Vector(-node.position.y, 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.x / abs(node.velocity.x)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.x > 1:
            node_force_normal.add(Vector(1 - node.position.x, 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.y / abs(node.velocity.y)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.y > 1:
            node_force_normal.add(Vector(1 - node.position.y, 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.x / abs(node.velocity.x)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))