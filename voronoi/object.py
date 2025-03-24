import math
from dataclasses import dataclass


@dataclass(frozen=True, eq=True) # Freeze class to make it hashable
class Point:
    x: float
    y: float

    def __eq__(self, obj: object):
        return self.x == obj.x and self.y == obj.y


@dataclass(frozen=True, eq=True)  # Freeze class to make it hashable
class Edge:
    a: Point
    b: Point

    def __eq__(self, obj: object):
        return self.a == obj.a and self.b == obj.b or self.a == obj.b and self.b == obj.a



class Triangle:
    def __init__(self, a: Point, b: Point, c: Point):
        self.points = [a, b, c]
        self.edges = [Edge(self.points[0], self.points[1]), Edge(self.points[0], self.points[2]), Edge(self.points[1], self.points[2])]
        self.ccx, self.ccy, self.ccr = self.__get_circumcircle()

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
        print(f"circle computed at x:{upx} y:{upy} radius:{radius}")

        return ux, uy, radius

    def circumcircle_has_point(self, p: Point) -> bool:
        dist = math.sqrt((self.ccx - p.x) ** 2 + (self.ccy - p.y) ** 2)
        return dist <= self.ccr

    def get_circumcircle_centre(self):
        return Point(self.ccx, self.ccy)
