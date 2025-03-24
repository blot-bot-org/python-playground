from copy import copy
from random import randint

import matplotlib.pyplot as plt
from func import *
from networkx import Graph, draw
from object import *
from PIL import Image, ImageDraw

points = gen_points(70, 100, 700)
supertri = get_super_triangle(points)

triangulation: set[Triangle] = {supertri}
remaining_points = copy(points)

i = 0
for p in points:
    i += 1
    print(f"{i} is i")

    remaining_points.remove(p)
    bad_triangles = set()
    polygon = set()

    for tri in triangulation:
        if tri.circumcircle_has_point(p):
            bad_triangles.add(tri)

    all_edges = []
    for tri in bad_triangles:
        all_edges.extend(tri.edges)

    for edge in all_edges:
        if all_edges.count(edge) == 1:
            polygon.add(edge)

    for tri in bad_triangles:
        triangulation.remove(tri)

    for edge in polygon:
        new_tri = Triangle(edge.a, edge.b, p)
        triangulation.add(new_tri)

tris = set(triangulation)
hull = []

for tri in triangulation:
    for p in supertri.points:
        if tri.has_point(p) and tri in tris:
            points_ = tri.points
            i = points_.index(p)
            ps = points_[:i] + points_[i+1:]
            hull.append(Edge(*ps))

            tris.remove(tri)

h = set(hull)
for e in hull:
    if e.a in supertri.points or e.b in supertri.points:
        # h.remove(e)
        pass


image = Image.new("RGBA", size=(800, 800), color=(0, 0, 0, 255))
image_draw = ImageDraw.Draw(image)

"""
drawing hull and triangles

for hull_edge in h:
    image_draw.line((hull_edge.a.x, hull_edge.a.y, hull_edge.b.x, hull_edge.b.y), fill="yellow")
    pass

for tri in tris:
    for edge in tri.edges:
        # image_draw.line((edge.a.x, edge.a.y, edge.b.x, edge.b.y))
        pass

# image.show()
"""


voronoi_graph_edges = []

map2 = {}
for tri in tris:
    for edge in tri.edges:
        for tri2 in tris:
            if edge in tri2.edges:
                voronoi_graph_edges.append(Edge(tri.get_circumcircle_centre(), tri2.get_circumcircle_centre()))
"""
map = {}
for tri in tris:
    for edge in tri.edges:
        map[edge.a] = []
        map[edge.b] = []

for tri in tris:
    for edge in tri.edges:
        map[edge.a].append(edge)
        map[edge.b].append(edge)

# for e in voronoi_graph_edges:
#     image_draw.line((e.a.x, e.a.y, e.b.x, e.b.y), fill="white")
#     pass

#for p in points:
#    image_draw.circle((p.x, p.y), radius=3, fill="red")
#
for (point, edges) in map.items():
    for e in edges:
        image_draw.line((e.a.x, e.a.y, e.b.x, e.b.y), fill=(60, 60, 60))
"""


for triangle in tris:
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    for e in triangle.edges:
        image_draw.line((e.a.x, e.a.y, e.b.x, e.b.y), fill=color)

for p in points:
    image_draw.circle((p.x, p.y), radius=3, fill="red")

"""
for every triangle
    add the triangle to graph

for every triangle
    get neighbouring triangles
    add edge between neighbour and triangle

for every triangle
    if not 3 neighbours (meaning 2 or less):
        remove triangle
"""



image.show()
