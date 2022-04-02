from time import sleep
from scipy.constants import g
import pygame
from softbodies import Softbody, Node, Link, Point
from structures import Tower, Pyramid, Blob

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
softbody = Tower(position=Point(0, 0), size=(3, 7), grid=(3, 7), mass=100, stiffness=2000, dampening=0.1)
#softbody = Pyramid(position=Point(0, 0), size=(2, 2), grid=3, mass=1, stiffness=100, dampening=0)
#softbody = Blob(position=Point(0, 0), size=2)
camera_position = Point(0, 0)
camera_zoom = 0.1


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

    for n in range(5):
        for node in softbody.nodes:
            node.force.set(Point(0, -node.mass * g))
        for link in softbody.links:
            force = link.get_force()
            link.nodes[0].force.add(
                force * (link.nodes[0].position - link.nodes[1].position) / Point.dist(link.nodes[0].position,
                                                                                       link.nodes[1].position))
            link.nodes[1].force.add(
                force * (link.nodes[1].position - link.nodes[0].position) / Point.dist(link.nodes[0].position,
                                                                                       link.nodes[1].position))
        softbody.nodes[0].force.set(Point(0, 0))
        softbody.nodes[8].force.set(Point(0, 0))
        softbody.nodes[16].force.set(Point(0, 0))
        softbody.nodes[24].force.add(Point(softbody.nodes[24].mass * g * 2, softbody.nodes[24].mass * g * 5))
        softbody.iterate(time=0.005)

    screen.fill((0, 0, 0))

    for link in softbody.links:
        pygame.draw.line(screen, color=(0, 0, 255), start_pos=transformed(link.nodes[0].position), end_pos=transformed(link.nodes[1].position), width=3)

    for node in softbody.nodes:
        pygame.draw.circle(screen, color=(255, 0, 0), center=transformed(node.position), radius=3)

    pygame.display.flip()
    sleep(1 / 30)