import math
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, eq=True) # Freeze class to make it hashable
class Point:
    x: float
    y: float

    def __eq__(self, obj: object):
        return self.x == obj.x and self.y == obj.y

    def __hash__(self) -> int:
        return hash(frozenset([self.x, self.y]))

@dataclass(frozen=True, eq=True)  # Freeze class to make it hashable
class Edge:
    a: Point
    b: Point

    def __eq__(self, obj: object):
        return self.a == obj.a and self.b == obj.b or self.a == obj.b and self.b == obj.a

    def __hash__(self) -> int:
        return hash(frozenset([self.a, self.b]))

def segments_intersect(edge1, edge2): # returns none if no intersection
    # Extract coordinates for convenience
    x1, y1 = edge1.a.x, edge1.a.y
    x2, y2 = edge1.b.x, edge1.b.y
    x3, y3 = edge2.a.x, edge2.a.y
    x4, y4 = edge2.b.x, edge2.b.y

    # Calculate the denominator
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # If denominator is zero, lines are parallel or coincident.
    # For simplicity, we return False here (assuming overlapping segments do not count).
    if denominator == 0:
        return False

    # Calculate t and u parameters using the derived formula
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
    u = ((x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)) / denominator

    # t and u should be between 0 and 1 (inclusive) for segments to intersect
    if not ( 0 <= t <= 1 and 0 <= u <= 1 ):
        return None

    intersection_x = x1 + t * (x2 - x1)
    intersection_y = y1 + t * (y2 - y1)

    return Point(intersection_x, intersection_y)

def point_inside_polygon(point: Point, edge: Edge):
    # uses an even odd ray intersection
    
    if edge.a.y > edge.b.y:
        edge = Edge(edge.b, edge.a)

    # Extract coordinates
    px, py = point.x, point.y
    x1, y1, x2, y2 = edge.a.x, edge.a.y, edge.b.x, edge.b.y

    # Ignore horizontal edges (they don't contribute to vertical crossings)
    if y1 == y2:
        return False

    # Handle precision issues: if py is exactly at y1 or y2, move it slightly
    if py == y1 or py == y2:
        py += 1e-9

    # Check if the point's y is between the edge's y-range
    if y1 <= py < y2:  
        # Compute intersection x using line equation
        x_intersection = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
        return px < x_intersection  # True if the intersection is to the right

    return False  # No intersection


def is_point_inside_voronoi_cell(point: Point, edges: list[Edge]) -> bool:
    """Returns True if the point is inside the Voronoi cell defined by its edges."""
    intersection_count = sum(point_inside_polygon(point, edge) for edge in edges)
    return intersection_count % 2 == 1  # Odd count = inside, even count = outside


class Triangle:
    def __init__(self, a: Point, b: Point, c: Point):
        self.points = [a, b, c]
        self.edges = [Edge(self.points[0], self.points[1]), Edge(self.points[0], self.points[2]), Edge(self.points[1], self.points[2])]
        self.ccx, self.ccy, self.ccr = self.__get_circumcircle()

        self.adjacant = []
        self.convex_edges = []

    def calculate_adjacant(self, triangle_mesh: list[Self]):
        for tri in triangle_mesh:
            if tri == self:
                continue

            for edge in self.edges:
                if tri.has_edge(edge) and not tri in self.adjacant:
                    self.adjacant.append(tri)
                    self.convex_edges.append(edge)

        self.convex_edges = [edge for edge in self.edges if edge not in self.convex_edges] # invert it, since we actually did all processed edges
        if len(self.convex_edges) > 1:
            print("ERROR! multiple convex edges")
            exit(1)

    def has_point(self, p: Point):
        return p in self.points

    # returns x, y, radius
    def __get_circumcircle(self):
        # https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        # using the method where all vectors are localised to the cartesian equation
        # compute aprime, bprime, cprime, split into components
        bpx, bpy = self.points[1].x - self.points[0].x, self.points[1].y - self.points[0].y
        cpx, cpy = self.points[2].x - self.points[0].x, self.points[2].y - self.points[0].y
        prime_d = 2 * (bpx * cpy - bpy * cpx)

        if prime_d == 0:
            prime_d = 1

        upx = (1 / prime_d) * (
                    cpy * (math.pow(bpx, 2) + math.pow(bpy, 2)) - bpy * (math.pow(cpx, 2) + math.pow(cpy, 2)))
        upy = (1 / prime_d) * (
                    bpx * (math.pow(cpx, 2) + math.pow(cpy, 2)) - cpx * (math.pow(bpx, 2) + math.pow(bpy, 2)))

        # delocalised cartesian coordinates
        ux = upx + self.points[0].x
        uy = upy + self.points[0].y

        # ||U'||
        radius = math.sqrt(math.pow(upx, 2) + math.pow(upy, 2))

        return ux, uy, radius

    def circumcircle_has_point(self, p: Point) -> bool:
        dist = math.sqrt((self.ccx - p.x) ** 2 + (self.ccy - p.y) ** 2)
        return dist <= self.ccr

    def get_circumcenter(self):
        return Point(self.ccx, self.ccy)

    def has_edge(self, edge: Edge):
        return self.edges[0] == edge or self.edges[1] == edge or self.edges[2] == edge


