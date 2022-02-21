import pygame
from softbodies import Softbody, Node, Link, Point

nodes = [[Node(mass=1, position=Point(x / 4, y / 4), velocity=Point(0, 0)) for y in range(5)] for x in range(5)]
softbody = Softbody(nodes=[node for node_buffer in nodes for node in node_buffer],
                    links=[])

for x in range(len(nodes)):
    for y in range(len(nodes[0]) - 1):
        softbody.links.append(Link(nodes[x][y], nodes[x][y + 1]))

for y in range(len(nodes[0])):
    for x in range(len(nodes) - 1):
        softbody.links.append(Link(nodes[x][y], nodes[x + 1][y]))

minimum = Point(-5, -5)
maximum = Point(5, 5)


def transform(point: Point) -> Point:
    return Point(500 * (point.x - minimum.x) / (maximum.x - minimum.x), 500 * (point.y - minimum.y) / (maximum.y - minimum.y))


pygame.init()
screen = pygame.display.set_mode([500, 500])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    for node in softbody.nodes:
        transformed = transform(node.position)
        pygame.draw.circle(screen, (0, 0, 255), (transformed.x, transformed.y), 3)

    softbody.iterate(0.001)
    softbody.nodes[0].position = Point(-1, -1)

    pygame.display.flip()

pygame.quit()