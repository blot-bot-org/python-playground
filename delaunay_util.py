import random
import math

# https://github.com/abbottjord94/python-delaunay/blob/main/python_delaunay.py
# https://en.wikipedia.org/wiki/Delaunay_triangulation
# https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/

class Triangle:
    def __init__(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c

    def point_in_circumcircle(self, x, y):
        # https://en.wikipedia.org/wiki/Delaunay_triangulation#Algorithms
        # matrix determinant
        pass

    def get_circumcircle(self):
        # https://en.wikipedia.org/wiki/Circumcircle#Cartesian_coordinates_2
        # using the method where all vectors are localised to the cartesian equation

        # compute aprime, bprime, cprime, split into components
        apx, apy = 0, 0
        bpx, bpy = self.b[0] - self.a[0], self.b[1] - self.a[1]
        cpx, cpy = self.c[0] - self.a[0], self.c[1] - self.a[1]
        prime_d = 2 * (bpx * cpy - bpy * cpx)

        upx = (1 / prime_d) * (cpy * (math.pow(bpx, 2) + math.pow(bpy, 2)) - bpy * (math.pow(cpx, 2) + math.pow(cpy, 2)))
        upy = (1 / prime_d) * (bpx * (math.pow(cpx, 2) + math.pow(cpy, 2)) - cpx * (math.pow(bpx, 2) + math.pow(bpy, 2)))

        # delocalised cartesian coordinates
        ux = upx + self.a[0]
        uy = upy + self.a[1]

        # ||U'||
        radius = math.sqrt(math.pow(upx, 2) + math.pow(upy, 2))
        print(f"circle computed at x:{upx} y:{upy} radius:{radius}")

        return (ux, uy, radius)


tri = Triangle((0, 0), (0, 10), (10, 5))
# (tri.get_circumcircle())




def gen_points(num, max_x, max_y) -> list[(int, int)]:
    points = []

    for i in range(num):
        points.append((random.randint(0, max_x), random.randint(0, max_y)))

    return points


# false: point_in_cornered_triangle(10, 10, 5, 5.00001)
# false: point_in_cornered_triangle(10, 10, 5, 5)
# true: point_in_cornered_triangle(10, 10, 5, 4.9999)
def point_in_cornered_triangle(triangle_width, triangle_height, x, y):
    triangle_gradient = (-triangle_height) / triangle_width
    y_height_at_x = triangle_gradient * x + triangle_height
    return y_height_at_x > y


# the super triangle is the triangle with it's right angle at the axis,
# with all points enclosed within the triangle
def find_super_triangle_w_h(points_):
    w = 1
    h = 1

    # create list of points, as points are within triangle, remove them
    points = points_
    # once list is empty, all points in triangle

    while len(points) > 0:
        i = 0
        while i < len(points):
            if point_in_cornered_triangle(w, h, points[i][0], points[i][1]):
                points.pop(i)
            else:
                w += 1
                h += 1
            i += 1

    return (w, h)


# print(find_super_triangle_w_h(gen_points(20, 100, 100)))
