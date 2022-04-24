from math import tau
from time import sleep
import cairo
import matplotlib.pyplot as plt
import numpy as np
from softbodies import Node, Link
from vectors import Vector


def render(nodes: list[Node], links: list[Link], camera_position: Vector, camera_zoom: float):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    ctx = cairo.Context(surface)

    ctx.scale(1000, 1000)
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
    ctx.translate(0.5, 0.5)
    ctx.scale(1, -1)
    ctx.scale(camera_zoom, camera_zoom)
    ctx.translate(-camera_position.x, -camera_position.y)

    for link in links:
        ctx.move_to(link.nodes[0].position.x, link.nodes[0].position.y)
        ctx.line_to(link.nodes[1].position.x, link.nodes[1].position.y)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.03 * (link.resting_length / link.get_length()))
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()

    for node in nodes:
        ctx.arc(node.position.x, node.position.y, 0.03, 0, tau)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.02)
        ctx.stroke()

    raw = surface.get_data().tolist()
    counter = 0
    image = np.empty((1000, 1000, 3), dtype=np.uint8)
    for x in range(1000):
        for y in range(1000):
            for c in range(3):
                image[x][y][2 - c] = raw[counter]
                counter += 1
            counter += 1
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.set_title("Propagated paths from transmitter to receiver")
    plt.show()

if __name__ == "__main__":
    print("This file is a utility program that does not work on its own.")
    sleep(5)
