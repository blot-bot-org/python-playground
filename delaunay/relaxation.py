import random

import networkx as nx
from PIL import Image, ImageDraw

from bowyer_watson import bowyer_watson
from structures import *

num_points = 1000
image = Image.open("../bird.png")
image = image.convert("RGB")
points = []

output = Image.new("RGBA", size=(round(image.width * 1.0), round(image.height * 1.0)), color=(0, 0, 0, 255))

while len(points) < num_points:
        x = random.randint(0, image.width - 1 - 0)
        y = random.randint(0, image.height - 1 - 0)
        greyscale = image.getpixel((x,y)) # as a tuple
        greyscale = 0.299 * greyscale[0] + 0.587 * greyscale[1] + 0.114 * greyscale[2]
        if greyscale < 50 or random.randint(0, 100) < 5:
            points.append(Point(x, y))


for i in range(0, 5):
    output = Image.new("RGBA", size=(round(image.width * 1.0), round(image.height * 1.0)), color=(0, 0, 0, 255))
    output_draw = ImageDraw.Draw(output)
    
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


    voronoi_verticies.extend(cyclical_intersects)
    for v in voronoi_verticies[:]:
        if v.x > image.width or v.x < 0 or v.y > image.height or v.y < 0:
            voronoi_verticies.remove(v)


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


# k so now i need a list of edges which form a polygon, and the associated site points
# this could be done by representing the tesselation as a graph, where the nodes are the verticies, and edges are edges (lol)
# then computing the polygons formed by the graph
# then finding the centroid of the polygon, and finding it's closest site point
# then associated said site point with the polygon


    def angle_with_x_axis(v1: Point, v2: Point) -> float:
        return math.atan2(v2.y - v1.y, v2.x - v1.x)



# remove duplicates in a bad not memory efficient aka "pythonic" way
    voronoi_edges = list(dict.fromkeys(voronoi_edges))
    voronoi_verticies = list(dict.fromkeys(voronoi_verticies))

    G = nx.DiGraph()

    for edge in voronoi_edges:
        G.add_edge(edge.a, edge.b)
        G.add_edge(edge.b, edge.a)

# map of vertex: empty list
    edges_by_vertex = {v: [] for v in G.nodes()}
    for u,v in G.edges():
        edges_by_vertex[u].append((v, angle_with_x_axis(u, v)))

    for v in edges_by_vertex:
        # sort by angle
        edges_by_vertex[v].sort(key=lambda x: x[1], reverse=True)

    used_edges = set()
    faces = []

    for u, edges in edges_by_vertex.items():
        for v, _ in edges:
            if (u, v) not in used_edges:
                face = []
                start = (u, v)
                current = start
                while True:
                    face.append(current[0])
                    used_edges.add(current)
                    v = current[1]
                    next_edges = edges_by_vertex[v]
                    for i in range(len(next_edges)):
                        if next_edges[i][0] == current[0]:
                            next_edge = next_edges[(i + 1) % len(next_edges)]
                            current = (v, next_edge[0])
                            break
                    if current == start:
                        break
                faces.append(face)


    for face in faces[:]:
        if (Point(0, 0) in face and Point(image.width, image.height) in face):
            faces.remove(face)
            print("removed superface")

    point_edges = {}

    for i in range(0, len(faces)):
        colour = (random.randint(100, 150), random.randint(100, 150), random.randint(100, 150))
    
        polygon_points = [point for point in faces[i]]
        edges = []
        for p in range(0, len(faces[i])):
            alternate_idx = p - 1 if p != 0 else len(faces[i]) - 1

            p1 = faces[i][p]
            p2 = faces[i][alternate_idx]

            edge = Edge(p1, p2)
            edges.append(edge)


        


        # THIS IS WHERE ITS ALL GOING TO GO BADLY!!!
        # basically, get the colour at each vertex, and an associated weight, darker is higher weight
        # when we average the points they converge more towards the weighted points
        point_weight = {}
        
        for v in polygon_points:
            vx = max(0, min(image.width - 1, round(v.x)))
            vy = max(0, min(image.height - 1, round(v.y)))

            pixel = image.getpixel((vx, vy))
            greyscale = 0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2]
            weight = 1 - greyscale / 254 # avoid divide by 0

            point_weight[v] = weight
            
        weighted_x = 0
        weighted_y = 0
        total_weight = 0

        for (point, weight) in point_weight.items():
            weighted_x += point.x * weight
            weighted_y += point.y * weight
            total_weight += weight

        centroid_x = weighted_x / total_weight
        centroid_y = weighted_y / total_weight

        site_point: Point = None
        for p in points:
            if is_point_inside_voronoi_cell(p, edges):
                site_point = p
                break

        if not site_point:
            # site point is none
            print("No site point!")
            point_edges[Point(centroid_x, centroid_y)] = edges
            continue


        # move site point towards centroid
        scale = 0.8
        newx = site_point.x + scale * (centroid_x - site_point.x)
        newy = site_point.y + scale * (centroid_y - site_point.y)
        output_draw.circle((newx, newy), radius=3, fill="white", outline="black")
        site_point = Point(newx, newy)

        point_edges[site_point] = edges


    points = list(point_edges.keys())


import numpy as np
from python_tsp.heuristics import solve_tsp_local_search

distance_matrix = np.empty((0, len(points)))

for j in range(len(points)):
    list = []
    for k in range(len(points)):
        dist = math.sqrt((points[j].x - points[k].x) ** 2 + (points[j].y - points[k].y) ** 2)
        list.append(dist)

    distance_matrix = np.vstack([distance_matrix, list])

print(distance_matrix)

permutation, distance = solve_tsp_local_search(distance_matrix)

print(len(permutation))
for i in range(0, len(permutation)):
    e = Edge(points[permutation[i]], points[permutation[(i + 1) % len(permutation)]])
    output_draw.line((e.a.x, e.a.y, e.b.x, e.b.y), fill="red")

with open("points.json", "w") as fp:
    fp.write("[")
    for p in points:
        fp.write(f"({p.x}, {p.y}), ")
    fp.write("]")

with open("permutations.json", "w") as fp:
    fp.write("[")
    for p in permutation:
        fp.write(f"{p}, ")
    fp.write("]")


output.show()
