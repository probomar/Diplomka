import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import os


def contact_z():
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_min], [0, 0, 0, 1]]))

    z_new = 0
    while True:
        flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
        collision, ncol = tibia.collision(flex)
        z_new += 1
        if ncol == 0:
            # flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            break

    print('z =', z_new * z_step + z_min)

    cor = open(file, 'a')
    cor.write(str(z_new * z_step + z_min))
    cor.write('\n')
    cor.close()


def max_contact_fiy(direction):
    fiy_new = 0
    while True:
        flex.rotate_y(direction, inplace=True)
        collision, ncol = tibia.collision(flex)
        fiy_new += 1
        if ncol != 0:
            break

    print('fi_y_new =', fiy_new)

    flex.rotate_y(-direction * fiy_new, inplace=True)
    return fiy_new


def contact_fiy_z(direction):
    z_new = 0
    fiy_new = 0
    while True:
        flex.rotate_y(direction, inplace=True)
        collision, fincol = tibia.collision(flex)
        if fincol != 0:
            flex.rotate_y(-1.5*direction, inplace=True)
            break
        fiy_new += direction
        z_new_p = 0

        while True:
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            collision, ncol = tibia.collision(flex)
            if ncol != 0:
                flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -2*z_step], [0, 0, 0, 1]]))
                break
            z_new_p -= 1
            z_new -= 1


def axis_of_rotation():
    # pm = np.array([10000, 10000, 10000])
    # pl = pm

    contact_volumes = tibia.boolean_intersection(flex)

    threshed = contact_volumes.threshold_percent([0.15, 0.50], invert=True)
    bodies = threshed.split_bodies()

    print(len(bodies), "\n")

    points_medial = np.empty((0, 3), int)
    points_lateral = np.empty((0, 3), int)

    for i in bodies.keys():
        point = np.array(bodies[i].center)
        if point[0] < 0:
            points_medial = np.append(points_medial, [np.array(bodies[i].center)], axis=0)
        else:
            points_lateral = np.append(points_lateral, [np.array(bodies[i].center)], axis=0)

    pm = np.mean(points_medial, axis=0)
    pl = np.mean(points_lateral, axis=0)

    if np.isnan(pm[0]):
        print('Medial point dont exist.')
    else:
        print('Medial point = ', pm)

    if np.isnan(pl[0]):
        print('Lateral point dont exist.\n')
    else:
        print('Lateral point = ', pl, "\n")

    axis = pl - pm

    return axis, pm, pl


def update_scene():
    axis, pm, pl = axis_of_rotation()
    flex.rotate_vector(vector=axis, angle=-fi_step, point=pl, inplace=True)
    old_axis = axis

    while True:
        axis, pm, pl = axis_of_rotation()
        if np.isnan(pm[0]) or np.isnan(pl[0]):
            flex.rotate_vector(vector=old_axis, angle=-0.1 * fi_step, point=pl, inplace=True)
        else:
            break

    p.update()


pv.global_theme.show_edges = True
z = 500
z_step = 0.1
z_min = -z_step * z / 2
z_range = z_step * z
fi = 500
fi_step = 3
file = 'cor.txt'
if os.path.exists(file):
    os.remove(file)

femur = pv.read('models/femur_mini.stl')
tibia = pv.read('models/tibia_mini.stl')

points = np.array([femur.points[0], femur.points[1], femur.points[58]])
# p2 = femur.points[100]
# p3 = femur.points[150]

# print(p1, p2, p3)
print(points)

flex = femur

contact_z()
max_fiy = max_contact_fiy(1)
min_fiy = max_contact_fiy(-1)
if max_fiy > min_fiy:
    contact_fiy_z(1)
else:
    contact_fiy_z(-1)
print('\n')

p = BackgroundPlotter(window_size=(800, 1000))

p.camera.position = (-300, 0, -10)
p.camera.focal_point = (100, 0, -10)

axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
axes.origin = (0, 0, 0)
p.add_actor(axes.actor)
p.add_mesh(flex)  #, style='wireframe')
p.add_mesh(tibia)  #, style='wireframe')
p.add_points(points, render_points_as_spheres=True, point_size=50, color='red')

# p.add_callback(update_scene, interval=200, count=fi)
p.show()
p.app.exec()
