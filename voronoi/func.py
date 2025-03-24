import random

from object import *


def gen_points(num, min, max) -> list[Point]:
    points = []
    for i in range(num):
        points.append(Point(random.randint(min, max), random.randint(min, max)))

    return points

def get_super_triangle(points: list[Point]) -> Triangle:
    max_x = max(point.x for point in points) * 2
    max_y = max(point.y for point in points) * 2

    return Triangle(Point(0, 0), Point(max_x, 0), Point(0, max_y))

def edge_distance(p1: Point, p2: Point):
    return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))
