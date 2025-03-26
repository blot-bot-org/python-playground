from structures import *


def get_super_triangle(points: list[Point]) -> Triangle:
    max_x = max(point.x for point in points) * 2
    max_y = max(point.y for point in points) * 2

    return Triangle(Point(0, 0), Point(max_x, 0), Point(0, max_y))

def bowyer_watson(points):
    num_points = len(points)

    super_triangle = get_super_triangle(points)
    triangles: list[Triangle] = [super_triangle]

    for point in points:
        bad_triangles = []

        for tri in triangles:
            if tri.circumcircle_has_point(point):
                bad_triangles.append(tri)

        polygon = []
        bad_triangle_edges = []

        for bad_tri in bad_triangles:
            bad_triangle_edges.extend(bad_tri.edges)

        for edge in bad_triangle_edges:
            if bad_triangle_edges.count(edge) == 1:
                polygon.append(edge)

        for bad_tri in bad_triangles:
            triangles.remove(bad_tri)

        for edge in polygon:
            new_tri = Triangle(edge.a, edge.b, point)
            triangles.append(new_tri)

    for tri in triangles[:]:
        for p in super_triangle.points:
            if tri.has_point(p):
                triangles.remove(tri)
                break

    return triangles
