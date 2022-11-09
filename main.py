import pyvista as pv
import numpy as np


pv.global_theme.show_edges = True
z_range = 80
z_step = 0.005
fi_range = 5
fi_step = 1

condyle1 = pv.ParametricEllipsoid(6, 10, 5,  center=(0, 0, 5))
femur = condyle1
tib = pv.Plane(i_size=30, j_size=30)
tibia = tib.triangulate()

flex_p = femur
flex = femur
for fi in range(fi_range):
    axes = pv.Axes(show_actor=True, actor_scale=15.0, line_width=5)
    view = pv.Plotter()
    view.add_actor(axes.actor)
    view.view_yz()
    intersection = np.ones([z_range]) * 5
    flex_p.rotate_x(fi_step, inplace=True)
    flex_p.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -0.25], [0, 0, 0, 1]]))

    for z in range(z_range):
        flex_p.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
        collision, ncol = tibia.collision(flex_p)
        intersection[z] = ncol

    print(intersection)
    flex_p.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -0.5], [0, 0, 0, 1]]))

    a = np.where(intersection == 0)
    b = np.where(intersection > 0)

    if a[0][0] > b[0][0]:
        z_new = a[0][0] - 1
    else:
        z_new = b[0][0]

    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_new * z_step], [0, 0, 0, 1]]))
    actual_view = tibia + flex
    view.add_mesh(actual_view)
    view.show()
