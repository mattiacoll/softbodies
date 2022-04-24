from math import tau
from scipy.constants import g
import cairo
from structures import Softbody
from vectors import Vector


def render(softbody: Softbody, camera_position: Vector, camera_zoom: float):
    nodes, links = softbody

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

    surface.write_to_png(f"render.png")
