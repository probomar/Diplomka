import numpy as np
import pandas as pd
import math as m
import forces as f
from setup import *


def initialization():
    contact_z()
    max_fiy = max_contact_fiy(1)
    min_fiy = max_contact_fiy(-1)
    if max_fiy > min_fiy:
        contact_fiy_z(1)
    else:
        contact_fiy_z(-1)

    cor0 = open(file0, 'a')
    cor0.write(str('Flexion'))
    cor0.write('\n')
    cor0.close()


def update_scene():
    p1_1 = np.array(flex.points[14])
    p2_1 = np.array(flex.points[25])

    slip_rotation()
    # t.rolling(tibia, flex)
    # t.rolling_with_ligament(tibia, flex, ACL0)

    p1_2 = np.array(flex.points[14])
    p2_2 = np.array(flex.points[25])

    actual_axis_of_rotation(p1_1, p2_1, p1_2, p2_2)

    p.update()


def slip_rotation():
    pm, pl = before_rotation()
    line = pv.Line(pm, pl)
    p.add_mesh(line, color='c', line_width=2)
    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)

    pm_new, pl_new = before_rotation()
    v1 = pm - pl
    v2 = pm_new - pl_new
    displacement = pm - pm_new
    vector_of_rotation = np.cross(v1, v2)
    angle_of_rotation = m.acos(np.dot(v2, v1) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
    flex.transform(np.array([[1, 0, 0, displacement[0]], [0, 1, 0, displacement[1]], [0, 0, 1, displacement[2]],
                             [0, 0, 0, 1]]))
    flex.rotate_vector(vector=vector_of_rotation, angle=angle_of_rotation, point=pm, inplace=True)


def rolling():
    pm, pl = before_rotation()
    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)


def rolling_with_ligament(ACL0):
    pm, pl = before_rotation()
    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)
    f.force_equilibrium(ACL0)

    ACL1 = np.array(tibia.points[2])
    ACL2 = np.array(flex.points[138])
    p.add_mesh(pv.Line(ACL1, ACL2), color='r', line_width=2)


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
        flex.rotate_y(fiy_step * direction, inplace=True)
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

    flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -2 * z_step], [0, 0, 0, 1]]))

    print('\n')

    cor3.write('\n')
    cor3.close()


def before_rotation():
    cor4 = open(file0, 'a')

    a = 0

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

        bodies, points_medial, points_lateral = contact_volume()

        if (not points_medial.any()) and (a == 1):
            print('medial, z')
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            z -= z_step
            a = 0
        elif (not points_medial.any()) and (a != 1):
            print('medial')
            flex.rotate_y(- fiy_step, inplace=True)
            fiy -= fiy_step
            a = -1
        elif (not points_lateral.any()) and (a == -1):
            print('lateral, z')
            flex.transform(np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]]))
            z -= z_step
            a = 0
        elif (not points_lateral.any()) and (a != -1):
            print('lateral')
            flex.rotate_y(fiy_step, inplace=True)
            fiy += fiy_step
            a = 1
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

    return pm, pl


def contact_volume():
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
    return contact_volumes, points_medial, points_lateral


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

    axis_of_rotation = pd.DataFrame(np.append(pA, pB).reshape(1, 6))
    axis_of_rotation.to_csv(file, index=False, mode='a', header=False)
