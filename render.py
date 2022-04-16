from math import tau
from scipy.constants import g
import cairo
import ffmpeg
from structures import tower
from points import Point

softbody = tower(position=Point(0, 0), size=(1, 1), grid=(4, 4), mass=1, stiffness=100, dampening=0)
nodes, links = softbody

camera_position = Point(0, 0)
camera_zoom = 0.5

for i in range(1000):
    for node in nodes:
        node.force.set(Point(0, -node.mass * g))
    for link in links:
        link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Point.dist(link.nodes[0].position, link.nodes[1].position))
        link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Point.dist(link.nodes[0].position, link.nodes[1].position))
    nodes[0].force.set(Point(0, 0))
    for node in nodes:
        node.iterate(time=0.005)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
    ctx = cairo.Context(surface)

    ctx.scale(500, 500)
    ctx.rectangle(0, 0, 1, 1)
    ctx.set_source_rgb(1, 0.94, 0.79)
    ctx.fill()
    ctx.translate(0.5, 0.5)
    ctx.scale(1, -1)
    ctx.translate(-camera_position.x, -camera_position.y)
    ctx.scale(camera_zoom, camera_zoom)

    for link in links:
        ctx.move_to(link.nodes[0].position.x, link.nodes[0].position.y)
        ctx.line_to(link.nodes[1].position.x, link.nodes[1].position.y)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.03)
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

ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run()
