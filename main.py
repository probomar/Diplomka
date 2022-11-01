import pyvista as pv
import numpy as np


pv.global_theme.show_edges = True
distance = 0.001
z_range = 10
fi_range = 1

condyle1 = pv.ParametricEllipsoid(6, 10, 5,  center=(0, 0, 5))
femur = condyle1
tib = pv.Plane(i_size=30, j_size=30)
tibia = tib.triangulate()
knee = tibia + femur

axes = pv.Axes(show_actor=True, actor_scale=15.0, line_width=5)
view = pv.Plotter()
view.add_actor(axes.actor)
view.add_mesh(knee, color='yellow')
intersection = np.ones([z_range, fi_range])*5

flex = femur
for fi in range(fi_range):
    flex.rotate_x(2, inplace=False)

    for z in range(z_range):
        flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z/1-5], [0, 0, 0, 1]]))
        view.add_mesh(flex)
        collision, ncol = tibia.collision(flex)
        print(ncol)
        if tibia.collision(flex) == 0:
            intersection[z] = 0
        else:
            intersection[z] = 1
        flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -(z/1-5)], [0, 0, 0, 1]]))
    if np.where(intersection == 0) > np.where(intersection == 1)

print(intersection)
view.show()

