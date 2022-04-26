import os
from math import pi, tau
from random import random
import cairo
import ffmpeg
from structures import Structure, Tower, Pyramid, Wheel
from vectors import Vector


structure = Tower(width=0.1, height=0.5, grid=(1, 5), mass=0.1, stiffness=50, dampening=1)
structure.translate(Vector(0.5, 0.5))
structure.rotate(pi / 6, center=Vector(0.5, 0.5))
# softbody = pyramid(position=Vector(0.5, 0.6), width=0.5, grid=6, mass=0.1, stiffness=100, dampening=1)
# softbody = wheel(position=Vector(0.5, 0.5), radius=0.25, rings=3, slices=10, mass=0.1, stiffness=200, dampening=1)
nodes = structure.nodes
links = structure.links

ln = [link.length for link in links]
for node in nodes:
    node.velocity.x += 2
    node.velocity.y += 3

camera_position = Vector(0.5, 0.5)
camera_zoom = 0.9


for i in range(500):
    for s in range(10):
        for node in nodes:
            node.force.set(Vector(0, -9.8 * node.mass))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))

        for node in nodes:
            if node.position.x < 0:
                node.force.x += 500 * abs(node.position.x)
            if node.position.x > 1:
                node.force.x -= 500 * abs(1 - node.position.x)
            if node.position.y < 0:
                node.force.y += 500 * abs(node.position.y)
            if node.position.y > 1:
                node.force.y -= 500 * abs(1 - node.position.y)

        nodes[0].force.set(Vector(0, 0))
        nodes[0].velocity.set(Vector(0, 0))

        for node in nodes:
            node.integrate(time=0.0005)


    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
    context = cairo.Context(surface)

    context.scale(500, 500)
    context.rectangle(0, 0, 1, 1)
    context.set_source_rgb(1, 1, 1)
    context.fill()
    context.translate(0.5, 0.5)
    context.scale(1, -1)
    context.scale(camera_zoom, camera_zoom)
    context.translate(-camera_position.x, -camera_position.y)

    context.rectangle(0, 0, 1, 1)
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.01)
    context.stroke()

    for link in links:
        context.move_to(link.nodes[0].position.x, link.nodes[0].position.y)
        context.line_to(link.nodes[1].position.x, link.nodes[1].position.y)
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.01 * (link.length / link.get_length()))
        context.stroke()

    for node in nodes:
        context.arc(node.position.x, node.position.y, 0.01, 0, tau)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.005)
        context.stroke()

    surface.write_to_png(f"output/{i:06d}.png")


ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run(overwrite_output=True)
for png in os.scandir("output"):
    os.remove(png)
