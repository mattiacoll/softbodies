import os
from math import tau
from scipy.constants import g
import cairo
import ffmpeg
from structures import tower, pyramid, wheel
from vectors import Vector


#softbody = tower(position=Vector(0, 0), width=1, height=1, grid=(10, 10), mass=1, stiffness=100, dampening=1)
softbody = pyramid(position=Vector(0, 0), width=1, grid=6, mass=1, stiffness=100, dampening=1)
#softbody = wheel(position=Vector(0, 0), radius=0.5, rings=7, slices=10, mass=1, stiffness=400, dampening=1)
nodes, links = softbody

camera_position = Vector(0, 0)
camera_zoom = 0.5



for i in range(500):
    for s in range(5):
        for node in nodes:
            node.force.set(Vector(0, -node.mass * g))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
        nodes[0].force.set(Vector(0, 0))
        for node in nodes:
            node.integrate(time=0.001)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 250, 250)
    ctx = cairo.Context(surface)

    ctx.scale(250, 250)
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(1, 0.94, 0.79)
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

    surface.write_to_png(f"output/{i:06d}.png")


ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run(overwrite_output=True)
for png in os.scandir("output"):
    os.remove(png)
