from time import sleep
from scipy.constants import g
import pygame
from softbodies import Softbody, Node, Link, Point
from structures import Tower, Pyramid

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
#softbody = Softbody(nodes=nodes, links=links)
#softbody = Tower(position=Point(0, 0), size=(4, 4), grid=(7, 7), mass=1, stiffness=50, dampening=0)
softbody = Pyramid(position=Point(0, 0), size=(2, 2), grid=7, mass=1, stiffness=1000, dampening=0)
print(len(softbody.links))
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

    for node in softbody.nodes:
        node.apply_force(force=Point(0, -node.mass * g))
    softbody.apply_link_forces()

    for n, node in enumerate(softbody.nodes):
        if n == 0:
            node.force.set(Point(0, 0))
            continue
        node.iterate(delta_time=0.01)


    screen.fill((0, 0, 0))

    for link in softbody.links:
        pygame.draw.line(screen, color=(0, 0, 255), start_pos=transformed(link.nodes[0].position), end_pos=transformed(link.nodes[1].position), width=3)

    for node in softbody.nodes:
        pygame.draw.circle(screen, color=(255, 0, 0), center=transformed(node.position), radius=3)

    pygame.display.flip()
    sleep(1 / 30)