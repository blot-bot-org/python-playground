from PIL import Image, ImageDraw
from delaunay_util import *
import matplotlib.pyplot as plt


# image_input = Image.Image.load("./penguin.jpg")


# list of int tuples, between xy:0-100
points: list[(int, int)] = gen_points(20, 100, 100)

supertriangle_w_h = find_super_triangle_w_h(points.copy())

image = Image.new("RGB", size=(300, 300))
image_draw = ImageDraw.Draw(image)
"""
image_draw.line([(0, supertriangle_w_h[1]), (supertriangle_w_h[0], 0)], width=2)
for p in points:
    print(f"{p[0]} {p[1]}")
    image_draw.point((p[0], p[1]), (255, 0, 0))
"""

triangle = Triangle((20, 20), (0, 50), (160, 120))
x, y, radius = triangle.get_circumcircle()
image_draw.circle((x, y), radius, fill="black", outline="white")

image_draw.point((x, y), (0, 255, 0))
image_draw.point((20, 20), (255, 0, 0))
image_draw.point((160, 120), (255, 0, 0))
image_draw.point((0, 50), (255, 0, 0))

image.show()