import random

import numpy as np
from PIL import Image, ImageDraw

from delaunay2D import Delaunay2D

num_points = 4000

points = []
delaunay, voronoi = None, None
iters = 0

image = Image.open("./bird.png")


output = Image.new("RGBA", size=(image.width, image.height), color=(0, 0, 0, 255))
output_draw = ImageDraw.Draw(output)


points = np.random.random((10, 2))

while len(points) < num_points:
    x = random.randint(0, image.width - 1)
    y = random.randint(0, image.height - 1)

    if sum(image.getpixel((x, y))) > 650 or random.random() < 0.001:
        #points.append((x, y))
        pass

for xy in points:
    output_draw.circle((xy[0], xy[1]), radius=2)



while iters < 1:
    iters += 1
    
    delaunay = Delaunay2D()
    for point in points:
        delaunay.addPoint(point)
