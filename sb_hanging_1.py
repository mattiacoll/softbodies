import os
from math import tau, sqrt
import cairo
import ffmpeg
from structures import Tower
from vectors import Vector

input_s = 0.5

while True:
    try:
        data = input("ENTER LINK STIFFNESS (0-1): ")
        input_s = float(data)
        if 0 <= input_s <= 1:
            break
        else:
            print("VALUE NOT BETWEEN THE SPECIFIED RANGE.")
        continue
    except ValueError:
        print("VALUE IS INVALID.")
        continue

input_d = 0.5

while True:
    try:
        data = input("ENTER LINK DAMPENING (0-1): ")
        input_d = float(data)
        if 0 <= input_d <= 1:
            break
        else:
            print("VALUE NOT BETWEEN THE SPECIFIED RANGE.")
        continue
    except ValueError:
        print("VALUE IS INVALID.")
        continue

os.makedirs("output", exist_ok=True)
for png in os.scandir("output"):
    os.remove(png)

time = 5
iterations = 10000
f = 0
camera_position = Vector(0.5, 0.5)
camera_zoom = 0.9
softbody = Tower(width=0.5, height=0.5, grid=(5, 5), mass=1, stiffness=400 * input_s ** 2, dampening=5 * input_d ** 2)
softbody.translate(Vector(0.5, 0.5))
nodes = softbody.nodes
links = softbody.links

print()
for i in range(iterations):
    print(f"SOLVING DIFFERENTIAL EQUATIONS: {round(100 * (i + 1) / iterations)}%", end="\r")
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
        if node.position.x < 0:
            node_force_normal.add(Vector(-500 * node.position.x, 0))
        if node.position.y < 0:
            node_force_normal.add(Vector(0, -500 * node.position.y))
        if node.position.x > 1:
            node_force_normal.add(Vector(500 * (1 - node.position.x), 0))
        if node.position.y > 1:
            node_force_normal.add(Vector(0, 500 * (1 - node.position.y)))
        node.force.add(node_force_normal)
    softbody.nodes_tower[0][-1].force.set(Vector(0, 0))
    for node in nodes:
        node.acceleration = node.force / node.mass
        node.velocity.add(node.acceleration * (time / iterations))
        node.position.add(node.velocity * (time / iterations))
    if i % round(iterations / time / 60) == 0:
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1000, 1000)
        context = cairo.Context(surface)
        context.scale(1000, 1000)
        context.rectangle(0, 0, 1, 1)
        context.set_source_rgb(0.29, 0.17, 0)
        context.fill_preserve()
        gradient = cairo.RadialGradient(0.5, 0.5, 0, 0.5, 0.5, sqrt(2) / 2)
        gradient.add_color_stop_rgba(0, 0, 0, 0, 0)
        gradient.add_color_stop_rgba(1, 0, 0, 0, 0.2)
        context.set_source(gradient)
        context.fill()
        context.translate(0.5, 0.5)
        context.scale(1, -1)
        context.scale(camera_zoom, camera_zoom)
        context.translate(-camera_position.x, -camera_position.y)

        context.rectangle(0, 0, 1, 1)
        context.set_source_rgb(0.5, 0.94, 1)
        context.fill_preserve()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(0.01)
        context.stroke()

        for link in links:
            context.move_to(link.nodes[0].position.x, link.nodes[0].position.y)
            context.line_to(link.nodes[1].position.x, link.nodes[1].position.y)
            context.set_source_rgb(0.5 * abs(link.get_force()), 0, 0)
            context.set_line_width(0.01 * (link.length / link.get_length()))
            context.stroke()

        for node in nodes:
            context.arc(node.position.x, node.position.y, 0.01, 0, tau)
            context.set_source_rgb(1, 1, 1)
            context.fill_preserve()
            if node is softbody.nodes_tower[0][-1]:
                context.set_source_rgb(1, 0, 0)
            else:
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