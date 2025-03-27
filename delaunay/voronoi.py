import random

from PIL import Image, ImageDraw

from bowyer_watson import bowyer_watson
from structures import *

num_points = 50
image = Image.open("../bird.png")
output = Image.new("RGBA", size=(round(image.width * 1.2), round(image.height * 1.2)), color=(0, 0, 0, 255))
output_draw = ImageDraw.Draw(output)
points = []

while len(points) < num_points:
    x = random.randint(100, image.width - 1 - 100)
    y = random.randint(100, image.height - 1 - 100)
    if sum(image.getpixel((x, y))) > 650 or random.random() < 0.1:
        points.append(Point(x, y))


for p in points:
    output_draw.circle((p.x, p.y), radius=2)
    pass

triangles = bowyer_watson(points)
for tri in triangles:
    tri.calculate_adjacant(triangles)

draw_triangles = False
if draw_triangles:
    for tri in triangles:
        colour = "white"
        output_draw.line((tri.edges[0].a.x, tri.edges[0].a.y, tri.edges[0].b.x, tri.edges[0].b.y), fill=colour)
        output_draw.line((tri.edges[1].a.x, tri.edges[1].a.y, tri.edges[1].b.x, tri.edges[1].b.y), fill=colour)
        output_draw.line((tri.edges[2].a.x, tri.edges[2].a.y, tri.edges[2].b.x, tri.edges[2].b.y), fill=colour)


site_points = []
for tri in triangles:
    site_points.append(tri.get_circumcenter())

for s in site_points:
    # output_draw.circle((s.x, s.y), radius=2)
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

# this can be optimise
voronoi_edges = list(dict.fromkeys(voronoi_edges))


for tri in triangles:
    for edge in tri.convex_edges:
        ab_x, ab_y = (edge.b.x - edge.a.x, edge.b.y - edge.a.y)
        perp_x, perp_y = (-ab_y, ab_x)

        cc = tri.get_circumcenter()
        length = 200
        point_b = Point(cc.x + length * perp_x, cc.y + length * perp_y)
        point_c = Point(cc.x + -length * perp_x, cc.y + -length * perp_y)

        perp_edge = Edge(cc, point_b)
        perp_edge_2 = Edge(cc, point_c)
        # output_draw.line((perp_edge.a.x, perp_edge.a.y, perp_edge.b.x, perp_edge.b.y), fill="yellow")
        # output_draw.line((perp_edge_2.a.x, perp_edge_2.a.y, perp_edge_2.b.x, perp_edge_2.b.y), fill="blue")

        # both sides, check which one intersects more to see which one to remove
        intersect = 0
        intersect_2 = 0

        for e in voronoi_edges:
            if (segments_intersect(e, perp_edge)):
                intersect += 1
            if (segments_intersect(e, perp_edge_2)):
                intersect_2 += 1

        if intersect_2 < intersect:
            voronoi_edges.append(perp_edge_2)
        else:
            voronoi_edges.append(perp_edge)



# so basically a few things here:
#   - find all intersects with bound edges, clockwise edges
#   - for each individual list, sort by size (so all points are clockwise)
#   - create new edge between each point pair

bounds = [
    (Edge(Point(0, 0), Point(image.width, 0)), False),
    (Edge(Point(image.width, 0), Point(image.width, image.height)), False),
    (Edge(Point(image.width, image.height), Point(0, image.height)), True),
    (Edge(Point(0, image.height), Point(0, 0)), True)
]
cyclical_intersects = []

for bound, rev in bounds:
    intersections = [bound.a]
    for idx, edge in enumerate(voronoi_edges[:]):
        possible_intersect = segments_intersect(edge, bound)
        if possible_intersect:
            possible_intersect_rounded = Point(round(possible_intersect.x, 5), round(possible_intersect.y, 5))
            intersections.append(possible_intersect_rounded)

            if voronoi_edges[idx].a.x > image.width or voronoi_edges[idx].a.y > image.height:
                voronoi_edges[idx] = Edge(voronoi_edges[idx].b, possible_intersect_rounded)
            else:
                voronoi_edges[idx] = Edge(voronoi_edges[idx].a, possible_intersect_rounded)

    if len(intersections) <= 1:
        cyclical_intersects.extend(intersections)
    else:
        # now sort them to be in order
        same_var_x = intersections[0].x == intersections[1].x
        if same_var_x:
            cyclical_intersects.extend(sorted(list(dict.fromkeys(intersections)), key=lambda obj: obj.y, reverse=rev))
        else:
            cyclical_intersects.extend(sorted(list(dict.fromkeys(intersections)), key=lambda obj: obj.x, reverse=rev))


extra_edges = []
for i in range(0, len(cyclical_intersects)):
    next_point = cyclical_intersects[i + 1 if i + 1 != len(cyclical_intersects) else 0]
    if cyclical_intersects[i] == next_point:
        continue

    edge = Edge(next_point, cyclical_intersects[i])
    extra_edges.append(edge)

    perp_edge = extra_edges[len(extra_edges) - 1]
    # output_draw.line((perp_edge.a.x, perp_edge.a.y, perp_edge.b.x, perp_edge.b.y), fill="pink")
    voronoi_edges.append(perp_edge)

for edge in voronoi_edges[:]:
    if edge.a.x > image.width or edge.a.x < 0 or edge.a.y > image.height or edge.a.y < 0:
        voronoi_edges.remove(edge)
        continue
    if edge.b.x > image.width or edge.b.x < 0 or edge.b.y > image.height or edge.b.y < 0:
        voronoi_edges.remove(edge)

for edge in voronoi_edges:
    output_draw.line((edge.a.x, edge.a.y, edge.b.x, edge.b.y), fill="red")
    pass

output.show()
