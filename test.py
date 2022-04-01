from scipy.constants import g
import pygame
from softbodies import Softbody, Node, Link, Point

nodes = [Node(mass=1, position=Point(1, 1)),
         Node(mass=1, position=Point(1, -1)),
         Node(mass=1, position=Point(-1, -1)),
         Node(mass=1, position=Point(-1, 1))]
links = [Link(nodes=(nodes[0], nodes[1]), stiffness=100, dampening=1),
         Link(nodes=(nodes[1], nodes[2]), stiffness=100, dampening=1),
         Link(nodes=(nodes[2], nodes[3]), stiffness=100, dampening=1),
         Link(nodes=(nodes[3], nodes[0]), stiffness=100, dampening=1),
         Link(nodes=(nodes[0], nodes[2]), stiffness=100, dampening=1, resting_length=2),
         Link(nodes=(nodes[1], nodes[3]), stiffness=100, dampening=1, resting_length=2)]
softbody = Softbody(nodes=nodes, links=links)

camera_position = Point(0, 0)
camera_zoom = 0.2


def transformed(position: Point) -> tuple[float, float]:
    return (500 * (camera_zoom * (position.x - camera_position.x) + 0.5),
            500 - (500 * (camera_zoom * (position.y - camera_position.y) + 0.5)))


pygame.init()
screen = pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    softbody.apply_force(Point(0, -1 * g))
    softbody.apply_link_forces()

    for n, node in enumerate(softbody.nodes):
        if n == 3:
            node.force.set(Point(0, 0))
            continue
        node.iterate(delta_time=0.001)


    screen.fill((255, 255, 255))

    for link in softbody.links:
        pygame.draw.line(screen, color=(0, 0, 255), start_pos=transformed(link.nodes[0].position), end_pos=transformed(link.nodes[1].position), width=5)

    for node in softbody.nodes:
        pygame.draw.circle(screen, color=(255, 0, 0), center=transformed(node.position), radius=10)

    pygame.display.flip()