import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import os
import pandas as pd


def contact_z():
    z_new = 0
    while True:
        collision, ncol = tibia.collision(flex)
        if ncol == 0:
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            z_new -= z_step
        else:
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
            z_new += z_step
            collision, ncol = tibia.collision(flex)
            if ncol == 0:
                break

    cor1 = open(file0, 'a')
    cor1.write(str('Contact z = '))
    cor1.write(str(z_new))
    cor1.write('\n\n')
    cor1.close()

    print('contact_z=', z_new)


def max_contact_fiy(direction):
    fiy_new = 0
    while True:
        flex.rotate_y(fiy_step*direction, inplace=True)
        collision, ncol = tibia.collision(flex)
        fiy_new += direction * fiy_step
        if ncol != 0:
            break

    flex.rotate_y(-fiy_new, inplace=True)

    cor2 = open(file0, 'a')
    cor2.write(str('Max fiy = '))
    cor2.write(str(fiy_new))
    cor2.write('\n\n')
    cor2.close()

    print('max_contact_fiy ( direction=', direction, ')=', fiy_new)

    return fiy_new


def contact_fiy_z(direction):
    print('contact_fiy_z ( direction=', direction, ')')

    cor3 = open(file0, 'a')
    cor3.write(str('Contact fiy z ( direction='))
    cor3.write(str(direction))
    cor3.write(str(')'))
    cor3.write('\n')

    fiy_new = 0

    while True:
        flex.rotate_y(direction * fiy_step, inplace=True)
        collision, fincol = tibia.collision(flex)

        if fincol != 0:
            flex.rotate_y(-direction * fiy_step, inplace=True)
            break

        fiy_new += direction * fiy_step

        z_new = 0

        while True:
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            collision, ncol = tibia.collision(flex)

            if ncol != 0:
                flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_step], [0, 0, 0, 1]]))
                break

            z_new -= z_step

        print('fiy=', fiy_new, ' z=', z_new)

        cor3.write(str('    fiy = '))
        cor3.write(str(fiy_new))
        cor3.write(str(' dz = '))
        cor3.write(str(z_new))
        cor3.write('\n')

    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -2*z_step], [0, 0, 0, 1]]))

    print('\n')

    cor3.write('\n')
    cor3.close()


def actual_axis_of_rotation(p1_1, p2_1, p1_2, p2_2):
    p1 = np.mean([p1_1, p1_2], axis=0)
    p2 = np.mean([p2_1, p2_2], axis=0)

    n1 = p1_1 - p1_2
    n2 = p2_1 - p2_2

    d1 = -n1 @ p1
    d2 = -n2 @ p2

    a = (n2[0] * n1[2] - n1[0] * n2[2]) / (n1[1] * n2[2] - n2[1] * n1[2])
    b = (n1[2] * d2 - n2[2] * d1) / (n1[1] * n2[2] - n2[1] * n1[2])

    x1 = 30
    y1 = a * x1 + b
    z1 = ((- n1[0] - a * n1[1]) * x1 - b * n1[1] - d1) / n1[2]

    x2 = -30
    y2 = a * x2 + b
    z2 = ((- n1[0] - a * n1[1]) * x2 - b * n1[1] - d1) / n1[2]

    pA = np.array([x1, y1, z1])
    pB = np.array([x2, y2, z2])

    line = pv.Line(pA, pB)
    p.add_mesh(line, color='g', line_width=2)

    return pA, pB

    # p.add_points(p1_1, color='r')
    # p.add_points(p2_1, color='y')
    # p.add_points(p1_2, color='r')
    # p.add_points(p2_2, color='y')
    # plane1 = pv.Plane(center=p1, direction=n1, i_size=200, j_size=200)
    # plane2 = pv.Plane(center=p2, direction=n2, i_size=200, j_size=200)
    # p.add_mesh(plane1, color='r', style='wireframe')
    # p.add_mesh(plane2, color='y', style='wireframe')


def update_scene():
    cor4 = open(file0, 'a')

    while True:
        z = 0
        fiy = 0
        while True:
            collision, ncol = tibia.collision(flex)

            if ncol == 0:
                print('z')
                flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
                z -= z_step
            else:
                break

        contact_volumes = tibia.boolean_intersection(flex)
        threshed = contact_volumes.threshold(0.001, invert=True)
        bodies = threshed.split_bodies()

        points_medial = np.empty((0, 3), int)
        points_lateral = np.empty((0, 3), int)

        for i in bodies.keys():
            point = np.array(bodies[i].center)
            if point[0] < 0:
                points_medial = np.append(points_medial, [np.array(bodies[i].center)], axis=0)
            else:
                points_lateral = np.append(points_lateral, [np.array(bodies[i].center)], axis=0)

        if not points_medial.any():
            print('medial')
            flex.rotate_y(- fiy_step, inplace=True)
            fiy -= fiy_step
        elif not points_lateral.any():
            print('lateral')
            flex.rotate_y(fiy_step, inplace=True)
            fiy += fiy_step
        else:
            break

    print('dz=', z, ', fiy=', fiy)

    cor4.write(str('dz = '))
    cor4.write(str(z))
    cor4.write(str(', dfiy = '))
    cor4.write(str(fiy))
    cor4.write('\n')
    cor4.close()

    pm = np.mean(points_medial, axis=0)
    pl = np.mean(points_lateral, axis=0)

    # print('Medial points:', points_medial, "\n")
    # print(pm, '\n\n')
    # print('Lateral points', points_lateral, "\n")
    # print(pl, '\n\n')

    p1_1 = np.array(flex.points[14])
    p2_1 = np.array(flex.points[25])

    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)

    p1_2 = np.array(flex.points[14])
    p2_2 = np.array(flex.points[25])

    pA, pB = actual_axis_of_rotation(p1_1, p2_1, p1_2, p2_2)

    axis_of_rotation = pd.DataFrame(np.append(pA, pB).reshape(1, 6))
    axis_of_rotation.to_csv('cor.csv', index=False, mode='a', header=False)

    p.update()


z_step = 0.02
fiy_step = 0.05
fi = 500
fi_step = 2
fi_max = int(140/fi_step)

file0 = 'cor0.txt'
if os.path.exists(file0):
    os.remove(file0)

file = 'cor.csv'
if os.path.exists(file):
    os.remove(file)

pv.global_theme.show_edges = True

femur = pv.read('models/femur_mini.stl')
tibia = pv.read('models/tibia_mini.stl')

flex = femur

contact_z()
max_fiy = max_contact_fiy(1)
min_fiy = max_contact_fiy(-1)
if max_fiy > min_fiy:
    contact_fiy_z(1)
else:
    contact_fiy_z(-1)

p = BackgroundPlotter(window_size=(800, 1000))

p.camera.position = (-300, 0, -10)
p.camera.focal_point = (100, 0, -10)

axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
axes.origin = (0, 0, 0)
p.add_actor(axes.actor)

p.add_mesh(flex, style='wireframe')
p.add_mesh(tibia, style='wireframe')

print('Flexion')

cor0 = open(file0, 'a')
cor0.write(str('Flexion'))
cor0.write('\n')
cor0.close()

p.add_callback(update_scene, interval=200, count=fi_max)

p.show()
p.app.exec()
