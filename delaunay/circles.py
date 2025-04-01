import json
import math

from PIL import Image, ImageDraw

from structures import *

points = []
permutation = []

with open("./points.json", "r") as fp:
    str = (fp.read().strip().replace("(", "[").replace(")", "]"))
    str = str[0:len(str) - 3] + "]"
    tup = json.loads(str)

    for t in tup:
        print(t)
        points.append(Point(t[0], t[1]))

with open("./permutations.json", "r") as fp:
    str = (fp.read().strip())
    str = str[0:len(str) - 3] + "]"
    permutation = json.loads(str)


# okay we loaded things now lets get started


output = Image.new("RGBA", size=(round(1000), round(1000)), color=(255, 255, 255, 255))
draw = ImageDraw.Draw(output)

start_point = points[permutation[0]]
x, y = start_point.x, start_point.y

for idx in permutation[:-1]:
    point = points[idx]
    next_point = points[permutation[permutation.index(idx) + 1]]

    ux, uy = x, y
    vx, vy = point.x, point.y

    for i in range(0, 48):
        ox, oy = math.sin(i / (2 * math.pi)) * 6, math.cos(i / (2 * math.pi)) * 6
        draw.point((ox + ux, oy + uy), fill="black")
        pass

    for i in range(0, 48):
        draw.point((ux + (i/48) * (vx - ux), uy + (i/48) * (vy - uy)), fill="black")

    x, y = vx, vy



output.show()
