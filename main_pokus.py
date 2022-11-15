import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import sys


def update_scene():
    intersection = np.ones([z]) * 5
    flex.rotate_x(fi_step, inplace=True)
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_min], [0, 0, 0, 1]]))

    for _ in range(z):
        flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
        collision, ncol = tibia.collision(flex)
        intersection[_] = ncol

    # print(intersection)
    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_range], [0, 0, 0, 1]]))

    a = np.where(intersection == 0)
    b = np.where(intersection > 0)

    if b[0].size == z:
        sys.exit("z_range neni dostatecny")

    if a[0][0] > b[0][0]:
        z_new = a[0][0] - 1
    else:
        z_new = b[0][0]

    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_new * z_step], [0, 0, 0, 1]]))

    cor_z = z_new * z_step - z_min

    # print('corp =', cor)
    # c = cor[cor.shape[0]-1, 2] + z_new * z_step - z_min
    # print(c)
    # print(cor.shape[0])
    # d = np.append(cor, [[0, 0, c]], axis=0)
    # print(np.append(cor, [[0, 0, c]], axis=0))
    # print('cor =', d)
    # cor = d
    # print('cor =', d)


    p.update()


if __name__ == '__main__':
    pv.global_theme.show_edges = True
    z = 80
    z_step = 0.005
    z_min = -z_step * z / 2
    z_range = z_step * z
    fi = 20
    fi_step = 1

    condyle1 = pv.ParametricEllipsoid(6, 10, 5, center=(0, 0, 0))
    femur = condyle1
    # femur = pv.read('models/femur.stl')

    tib = pv.Plane(i_size=30, j_size=30, center=(0, 0, -5))
    tibia = tib.triangulate()
    # tibia = pv.read('models/tibia.stl')

    flex = femur
    # cor = flex.center
    # print(cor)
    # cor = np.array([0, 0, 0])
    # print(cor.shape)
    # cor = cor[np.newaxis, :]
    # print(cor.shape)
    # print(cor.shape[0])

    p = BackgroundPlotter(window_size=(1000, 600))

    p.camera.position = (-30, 0, 0)
    p.camera.focal_point = (10, 0, 0)

    p.add_mesh(flex, style='wireframe')
    p.add_mesh(tibia)
    # p.add_points(cor, render_points_as_spheres=True, point_size=10.0, color='red')

    p.add_callback(update_scene, interval=fi)

    p.show()
    p.app.exec_()
