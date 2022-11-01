import pyvista as pv
import numpy as np


pv.global_theme.show_edges = True
n = 20
z_range = 10

# condyle1 = pv.ParametricEllipsoid(6, 10, 5)
# condyle2 = pv.ParametricEllipsoid(5, 7, 5)
# transform_matrix = np.array([[1, 0, 0, 3], [0, 1, 0, -1], [0, 0, 1, 0], [0, 0, 0, 1]])
# femur = condyle1.transform(transform_matrix) + condyle2.transform(-transform_matrix)
# # femur.plot(show_edges=True)
# tibia = pv.Plane(i_size=30, j_size=30)
# # tibia.plot(show_edges=True)
# knee = tibia.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -5], [0, 0, 0, 1]])) + femur
# knee.plot(show_edges=True)


# condyle1 = pv.ParametricEllipsoid(6, 10, 5)
condyle1 = pv.Sphere(5, center=(0, 0, 5))
femur = condyle1
tib = pv.Plane(i_size=30, j_size=30)
tibia = tib.triangulate()
# tibia.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -5], [0, 0, 0, 1]]))
knee = tibia + femur
# knee.plot(show_edges=True)
print(tibia.bounds)

axes = pv.Axes(show_actor=True, actor_scale=15.0, line_width=5)
view = pv.Plotter()
view.add_actor(axes.actor)
view.add_mesh(knee, color='yellow')
intersection = np.ones(n)*5
# print(intersection)

flex = pv.Plotter()
flex.add_mesh(femur)
flex_axes = pv.Axes(show_actor=True, actor_scale=10.0, line_width=5)
axes.origin = (0, 0, -5.0)
flex.add_actor(flex_axes.actor)
for z in range(z_range):
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0.05], [0, 0, 0, 1]])) + femur
    flex = femur.rotate_x(1, point=axes.origin, inplace=False)
    view.add_mesh(flex)
    # print(tibia.boolean_intersection(flex).n_cells)
    if tibia.boolean_intersection(flex).n_cells == 0:
        intersection[z] = 0
    else:
        intersection[z] = 1
print(intersection)
view.show()


axes = pv.Axes(show_actor=True, actor_scale=2.0, line_width=5)
axes.origin = (3.0, 3.0, 3.0)
p.add_actor(axes.actor)