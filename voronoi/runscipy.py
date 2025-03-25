import matplotlib.pyplot as plt
from func import *
from scipy.spatial import Voronoi, voronoi_plot_2d

# Step 1: Define the seed points
points = [(point.x, point.y) for point in gen_points(100, 0, 2000)]


for i in range(0, 13):
    print(i)
# Step 2: Create the Voronoi diagram
    vor = Voronoi(points)



    polygons = []

    for point_index in range(len(vor.points)):
        point_xy = vor.points[point_index]
        region_idx = vor.point_region[point_index]
        region = vor.regions[region_idx]
        # Ensure the region is valid (not infinite)
        if len(region) > 0 and -1 not in region:
            # Get the vertices of the polygon
            polygon = [vor.vertices[i] for i in region]
            polygons.append((point_xy, polygon))


    if i == 12:
        voronoi_plot_2d(vor)


    new_points = []

    for point_xy, polygon in polygons:
        x = 0
        y = 0
        n = len(polygon)
        for edge in polygon:
            x += edge[0]
            y += edge[1]

        avg_x, avg_y = x / n, y / n
        if i == 0:
            print("hi")
            print(avg_x, avg_y)
        point_x, point_y = point_xy

        lerp_x = (avg_x - point_x / 2) + point_x
        lerp_y = (avg_y - point_y / 2) + point_y
        new_points.append((lerp_x, lerp_y))

    points = (new_points)

plt.show()
print("showing")
