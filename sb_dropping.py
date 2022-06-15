import os
from math import tau, sqrt
import cairo
import ffmpeg
from structures import Tower
from vectors import Vector

input_s = 0.5

while True:
    try:
        data = input("STIFFNESS (0-1) [0.5]: ")
        if data == "":
            break
        input_s = float(data) ** 2
        if 0 <= input_s <= 1:
            break
        continue
    except ValueError:
        print( "Value not valid, please insert a floating point number between 0 and 1" )
        continue

input_d = 0.5

while True:
    try:
        data = input("DAMPENING (0-1) [0.5]: ")
        if data == "":
            break
        input_d = float(data) ** 2
        if 0 <= input_d <= 1:
            break
        continue
    except ValueError:
        print( "Value not valid, please insert a floating point number" )
        continue

os.makedirs("output", exist_ok=True)
for png in os.scandir("output"):
    os.remove(png)

time = 5
iterations = 5000
f = 0
camera_position = Vector(0.5, 0.5)
camera_zoom = 0.9
softbody = Tower(width=0.5, height=0.5, grid=(7, 7), mass=1, stiffness=200 * input_s, dampening=2 * input_d)
softbody.translate(Vector(0.5, 0.5))
nodes = softbody.nodes
links = softbody.links

for i in range(iterations):
    for node in nodes:
        node.force.set(Vector(0, 0))
    for node in nodes:
        node.force.add(Vector(0, -9.8 * node.mass))
    for link in links:
        node_1 = link.nodes[0]
        node_2 = link.nodes[1]
        node_1_force = link.get_force() * (
                node_1.position - node_2.position
        ) / Vector.dist(node_1.position, node_2.position)
        node_1.force.add(node_1_force)
        node_2.force.sub(node_1_force)
    for node in nodes:
        node_force_normal = Vector(0, 0)
        node_force_friction = Vector(0, 0)
        if node.position.x < 0:
            node_force_normal.add(Vector(-500 * node.position.x, 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.y / abs(node.velocity.y)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.y < 0:
            node_force_normal.add(Vector(0, -500 * node.position.y))
            try:
                node_force_friction.add(Vector(0, -node.velocity.x / abs(node.velocity.x)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.x > 1:
            node_force_normal.add(Vector(500 * (1 - node.position.x), 0))
            try:
                node_force_friction.add(Vector(0, -node.velocity.y / abs(node.velocity.y)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        if node.position.y > 1:
            node_force_normal.add(Vector(0, 500 * (1 - node.position.y)))
            try:
                node_force_friction.add(Vector(0, -node.velocity.x / abs(node.velocity.x)))
            except ZeroDivisionError:
                node_force_friction.add(Vector(0, 0))
        node.force += node_force_normal + 0 * node_force_normal.len() * node_force_friction
    for node in nodes:
        node.acceleration = node.force / node.mass
        node.velocity.add(node.acceleration * (time / iterations))
        node.position.add(node.velocity * (time / iterations))
    if i % round(iterations / time / 60) == 0:
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 500, 500)
        context = cairo.Context(surface)
        context.scale(500, 500)
        context.rectangle(0, 0, 1, 1)
        gradient = cairo.RadialGradient(0.5, 0.5, 0, 0.5, 0.5, sqrt(2) / 2)
        gradient.add_color_stop_rgb(0, 1, 1, 1)
        gradient.add_color_stop_rgb(1, 0.8, 0.8, 0.8)
        context.set_source(gradient)
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

        surface.write_to_png(f"output/{f:06d}.png")
        f += 1

ffmpeg.input("output/%06d.png", pattern_type="sequence", framerate=60).output("output.mp4").run(overwrite_output=True)
for png in os.scandir("output"):
    os.remove(png)
os.rmdir("output")
os.startfile("output.mp4")