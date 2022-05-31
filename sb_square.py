import os
from math import pi, tau
from time import sleep
import cairo
import ffmpeg
from structures import Tower
from vectors import Vector

print("This program will simulate the physics of a softbody square mesh.")
sleep(1)
print("The object is dropped from a height of 0.5 meters and is then launched diagonally.")
sleep(1)

print("Enter the number of horizontal grid elements in the mesh.")
grid_x = 1
while True:
    try:
        grid_x = int(input("[1-7]: "))
        assert 1 <= grid_x <= 7
        break
    except:
        continue

print("Enter the number of vertical grid elements in the mesh.")
grid_y = 1
while True:
    try:
        grid_y = int(input("[1-7]: "))
        assert 1 <= grid_y <= 7
        break
    except:
        continue

print("Integrating Hooke's law twice...")

structure = Tower(width=0.1 * grid_x, height=0.1 * grid_y, grid=(grid_x, grid_y), mass=0.1, stiffness=50, dampening=1)
structure.translate(Vector(0.5, 0.5))
structure.rotate(pi / 12, center=Vector(0.5, 0.5))
nodes, links = structure.get_components()

camera_position = Vector(0.5, 0.5)
camera_zoom = 0.9


os.makedirs("output", exist_ok=True)
for png in os.scandir("output"):
    os.remove(png)

for i in range(250):
    if i == 100:
        for node in nodes:
            node.velocity.x += 3
            node.velocity.y += 5

    for s in range(10):
        for node in nodes:
            node.force.set(Vector(0, -9.8 * node.mass))
        for link in links:
            link.nodes[0].force.add(link.get_force() * (link.nodes[0].position - link.nodes[1].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))
            link.nodes[1].force.add(link.get_force() * (link.nodes[1].position - link.nodes[0].position) / Vector.dist(
                link.nodes[0].position, link.nodes[1].position))

        for node in nodes:
            force_normal = Vector(0, 0)
            if node.position.x < 0:
                force_normal.x += 100 * abs(node.position.x)
            elif node.position.x > 1:
                force_normal.x -= 100 * abs(1 - node.position.x)
            if node.position.y < 0:
                force_normal.y += 100 * abs(node.position.y)
            elif node.position.y > 1:
                force_normal.y -= 100 * abs(1 - node.position.y)
            try:
                force_friction = -0.25 * force_normal.len() * (node.velocity / node.velocity.len())
            except ZeroDivisionError:
                force_friction = Vector(0, 0)
            node.force += force_normal + force_friction

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
        amt = node.velocity.len()
        context.arc(node.position.x, node.position.y, 0.01, 0, tau)
        context.set_source_rgb(1, 1 - amt / 5, 1 - amt / 5)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.005)
        context.stroke()

    surface.write_to_png(f"output/{i:06d}.png")

ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run(overwrite_output=True)
for png in os.scandir("output"):
    os.remove(png)
os.rmdir("output")
os.startfile("output.mp4")