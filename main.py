import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import sys
import os


def contact_z():
    intersection = np.ones([z]) * 5
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_min], [0, 0, 0, 1]]))

    for _ in range(z):
        flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
        collision, ncol = tibia.collision(flex)
        intersection[_] = ncol

    print(intersection)
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_range], [0, 0, 0, 1]]))

    a = np.where(intersection == 0)
    b = np.where(intersection > 0)

    if b[0].size == z:
        sys.exit("rozsah z neni dostatecny")

    if a[0][0] > b[0][0]:
        z_new = a[0][0] - 1
    else:
        z_new = b[0][0]

    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_new * z_step], [0, 0, 0, 1]]))

    print('z_new =', z_new)
    print('z_step =', z_step)
    print('z_min =', z_min)

    print('z =', z_new * z_step + z_min)

    cor = open(file, 'a')
    cor.write(str(z_new * z_step + z_min))
    cor.write('\n')
    cor.close()


def update_scene():
    flex.rotate_vector(vector=(1, 0, 0), angle=-fi_step, point=axes.origin, inplace=True)

    contact_z()

    p.update()


if __name__ == '__main__':
    pv.global_theme.show_edges = True
    z = 500
    z_step = 0.1
    z_min = -z_step * z / 2
    z_range = z_step * z
    fi = 20
    fi_step = 5
    file = 'cor.txt'
    if os.path.exists(file):
        os.remove(file)

    femur = pv.read('models/femur_mini.stl')
    tibia = pv.read('models/tibia_mini.stl')

    flex = femur

    contact_z()

    p = BackgroundPlotter(window_size=(800, 1000))

    p.camera.position = (-300, 0, -10)
    p.camera.focal_point = (100, 0, -10)

    axes = pv.Axes(show_actor=True, actor_scale=100, line_width=20)
    axes.origin = (0, 0, 0)
    p.add_actor(axes.actor)
    p.add_mesh(flex, style='wireframe')
    p.add_mesh(tibia, style='wireframe')

    p.add_callback(update_scene, count=fi)

    p.show()
    p.app.exec_()
