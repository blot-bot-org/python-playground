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
    min_x = min(0, min(point.x for point in points) * 2)
    min_y = min(0, min(point.y for point in points) * 2)

    return Triangle(Point(min_x, min_y), Point(max_x, min_y), Point(min_x, max_y))

def edge_distance(p1: Point, p2: Point):
    return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))
