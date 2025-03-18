import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

from delaunay_util import *

# image_input = Image.Image.load("./penguin.jpg")


# list of int tuples, between xy:0-100
points: list[(int, int)] = gen_points(100, 100, 100)

supertriangle_w_h = find_super_triangle_w_h(points.copy())

image = Image.new("RGB", size=(300, 300))
image_draw = ImageDraw.Draw(image)
# image_draw.line([(0, supertriangle_w_h[1]), (supertriangle_w_h[0], 0)], width=2)

supertriangle_obj = Triangle((0, 0), (0, supertriangle_w_h[1]), (supertriangle_w_h[0], 0))

x, y, radius = supertriangle_obj.get_circumcircle()
image_draw.circle((x, y), radius, fill="black", outline="white")

image_draw.point((x, y), (0, 255, 0))
for p in points:
    print(f"{p[0]} {p[1]}")
    image_draw.point((p[0], p[1]), (255, 0, 0))

image.show()
