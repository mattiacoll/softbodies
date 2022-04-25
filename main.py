import os
from math import tau
import cairo
import ffmpeg
from structures import tower, pyramid, wheel
from vectors import Vector


#softbody = tower(position=Vector(0, 0), width=1, height=1, grid=(10, 10), mass=1, stiffness=100, dampening=1)
softbody = pyramid(position=Vector(0, 1), width=0.5, grid=6, mass=0.1, stiffness=100, dampening=1)
#softbody = wheel(position=Vector(0, 0), radius=0.5, rings=7, slices=10, mass=1, stiffness=400, dampening=1)
nodes, links = softbody


camera_position = Vector(0, 0)
camera_zoom = 1



for i in range(500):
    for s in range(5):
        for node in nodes:
            node.force.set(Vector(0, -9.8 * node.mass))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))

        for node in nodes:
            if node.position.y < 0:
                node.force.y -= 500 * node.position.y

        for node in nodes:
            node.integrate(time=0.001)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 250, 250)
    context = cairo.Context(surface)

    context.scale(250, 250)
    context.rectangle(0, 0, 1, 1)
    context.set_source_rgb(1, 0.94, 0.79)
    context.fill()
    context.translate(0.5, 0.5)
    context.scale(1, -1)
    context.scale(camera_zoom, camera_zoom)
    context.translate(-camera_position.x, -camera_position.y)

    context.rectangle(-1000, -10, 2000, 10)
    context.set_source_rgb(1, 1, 1)
    context.fill()
    context.move_to(-1000, 0)
    context.line_to(1000, 0)
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.01)
    context.stroke()

    for link in links:
        context.move_to(link.nodes[0].position.x, link.nodes[0].position.y)
        context.line_to(link.nodes[1].position.x, link.nodes[1].position.y)
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.01 * (link.resting_length / link.get_length()))
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        context.stroke()

    for node in nodes:
        context.arc(node.position.x, node.position.y, 0.01, 0, tau)
        context.set_source_rgb(1, 1, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.01)
        context.stroke()

    surface.write_to_png(f"output/{i:06d}.png")


ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run(overwrite_output=True)
for png in os.scandir("output"):
    os.remove(png)
