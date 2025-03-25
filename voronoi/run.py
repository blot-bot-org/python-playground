from copy import copy
from random import randint

import matplotlib.pyplot as plt
import networkx as nx
from func import *
from object import *
from PIL import Image, ImageDraw

points = gen_points(150, 0, 800)
supertri = get_super_triangle(points)

triangulation: set[Triangle] = {supertri}
remaining_points = copy(points)

i = 0
for p in points:
    i += 1
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
# print delaunay triangulation

for triangle in tris:
    color = (randint(100, 255), randint(100, 255), randint(100, 255))
    for e in triangle.edges:
        image_draw.line((e.a.x, e.a.y, e.b.x, e.b.y), fill=color)
    cc = triangle.get_circumcenter()
    #image_draw.circle((cc.x, cc.y), radius=3, fill=color)

for p in points:
    image_draw.circle((p.x, p.y), radius=3, fill="red")
    pass
"""



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

triangle_graph = nx.Graph()

print(len(tris))
triangle_graph.add_nodes_from([tri.get_circumcenter() for tri in tris]) # add all triangles' circumcenters

for ogtri in tris:
    for tri2 in tris:
        if ogtri == tri2:
            continue
        
        for edge in ogtri.edges:
            if tri2.has_edge(edge):
                weight = edge_distance(ogtri.get_circumcenter(), tri2.get_circumcenter())
                if weight < 10000: # this breaks things but it should be implemented properly at some point
                    triangle_graph.add_edge(ogtri.get_circumcenter(), tri2.get_circumcenter(), weight=weight)
                else:
                    print(ogtri.get_circumcenter(), tri2.get_circumcenter(), weight)

nodes_to_remove = [node for node in triangle_graph.nodes if triangle_graph.degree(node) < 2]
triangle_graph.remove_nodes_from(nodes_to_remove)

for n1, n2 in triangle_graph.edges():
    image_draw.line((n1.x, n1.y, n2.x, n2.y))
    pass

# single point <-> 
point_map = {}

for t in tris:
    image_draw.circle((t.points[0].x, t.points[0].y), radius=3, fill="red")
    image_draw.circle((t.points[1].x, t.points[1].y), radius=3, fill="red")
    image_draw.circle((t.points[2].x, t.points[2].y), radius=3, fill="red")




image.show()
