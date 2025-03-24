from object import *
import random

def gen_points(num, min, max) -> list[Point]:
    points = []
    for i in range(num):
        points.append(Point(random.randint(min, max), random.randint(min, max)))

    return points

def get_super_triangle(points: list[Point]) -> Triangle:
    max_x = max(point.x for point in points) * 2
    max_y = max(point.y for point in points) * 2

    return Triangle(Point(0, 0), Point(max_x, 0), Point(0, max_y))
