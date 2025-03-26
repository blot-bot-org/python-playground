import random

from PIL import Image, ImageDraw

from bowyer_watson import bowyer_watson
from structures import *

num_points = 50
image = Image.open("../bird.png")
output = Image.new("RGBA", size=(image.width, image.height), color=(0, 0, 0, 255))
output_draw = ImageDraw.Draw(output)
points = []

while len(points) < num_points:
    x = random.randint(100, image.width - 1 - 100)
    y = random.randint(100, image.height - 1 - 100)
    if sum(image.getpixel((x, y))) > 650 or random.random() < 0.1:
        points.append(Point(x, y))


for p in points:
    # output_draw.circle((p.x, p.y), radius=2)
    pass

triangles = bowyer_watson(points)
for tri in triangles:
    tri.calculate_adjacant(triangles)

draw_triangles = False
if draw_triangles:
    for tri in triangles:
        colour = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        output_draw.line((tri.edges[0].a.x, tri.edges[0].a.y, tri.edges[0].b.x, tri.edges[0].b.y), fill=colour)
        output_draw.line((tri.edges[1].a.x, tri.edges[1].a.y, tri.edges[1].b.x, tri.edges[1].b.y), fill=colour)
        output_draw.line((tri.edges[2].a.x, tri.edges[2].a.y, tri.edges[2].b.x, tri.edges[2].b.y), fill=colour)


site_points = []
for tri in triangles:
    site_points.append(tri.get_circumcenter())

for s in site_points:
    output_draw.circle((s.x, s.y), radius=2)
    pass




voronoi_verticies = [tri.get_circumcenter() for tri in triangles]
voronoi_edges = []

draw_voronoi = True
if draw_voronoi:
    for tri in triangles:
        for tri2 in tri.adjacant:
            clip_tri_circum = tri.get_circumcenter()
            clip_tri2_circum = tri2.get_circumcenter()
            voronoi_edges.append(Edge(clip_tri_circum, clip_tri2_circum))



for edge in voronoi_edges:
    output_draw.line((edge.a.x, edge.a.y, edge.b.x, edge.b.y), fill="red")
    pass

for tri in triangles:
    for edge in tri.convex_edges:
        output_draw.line((edge.a.x, edge.a.y, edge.b.x, edge.b.y), fill="green")

        ab_x, ab_y = (edge.b.x - edge.a.x, edge.b.y - edge.a.y)
        perp_x, perp_y = (-ab_y, ab_x)

        cc = tri.get_circumcenter()
        output_draw.circle((cc.x, cc.y), radius=2, fill="orange")
        alpha = 10
        point_b = Point(cc.x + 10 * perp_x, cc.y + 10 * perp_y)

        perp_edge = Edge(cc, point_b)
        output_draw.line((perp_edge.a.x, perp_edge.a.y, perp_edge.b.x, perp_edge.b.y), fill="yellow")




output.show()
