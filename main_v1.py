import pyvista as pv
import numpy as np


pv.global_theme.show_edges = True
distance = 0.001
z_range = 10
fi_range = 10

condyle1 = pv.Sphere(5, center=(0, 0, 5))
femur = condyle1
tib = pv.Plane(i_size=30, j_size=30)
tibia = tib.triangulate()
knee = tibia + femur

axes = pv.Axes(show_actor=True, actor_scale=15.0, line_width=5)
view = pv.Plotter()
view.add_actor(axes.actor)
view.add_mesh(knee, color='yellow')
intersection = np.ones([z_range, fi_range])*5
# print(intersection)


for z in range(z_range):
    flexp = femur
    flexp.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, distance], [0, 0, 0, 1]])) + femur
    flex_axes = pv.Axes(show_actor=True, actor_scale=10.0, line_width=5)
    flex_axes.origin = (0, 0, -z)

    for fi in range(fi_range):
        flex = flexp.rotate_x(2 * (fi + 1), point=axes.origin, inplace=False)
        view.add_mesh(flex)
        if tibia.boolean_intersection(flex).n_cells == 0:
            intersection[z, fi] = 0
        else:
            intersection[z, fi] = 1
        flex_axes.origin = (0, 0, z)

print(intersection)
view.show()



