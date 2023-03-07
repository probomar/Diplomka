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
    axis_of_rotation.to_csv('cor.csv', index=False, mode='a', header=False)

    # p.add_points(p1_1, color='r')
    # p.add_points(p2_1, color='y')
    # p.add_points(p1_2, color='r')
    # p.add_points(p2_2, color='y')
    # plane1 = pv.Plane(center=p1, direction=n1, i_size=200, j_size=200)
    # plane2 = pv.Plane(center=p2, direction=n2, i_size=200, j_size=200)
    # p.add_mesh(plane1, color='r', style='wireframe')
    # p.add_mesh(plane2, color='y', style='wireframe')


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


def before_rotation():
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

        bodies, points_medial, points_lateral = contact_volume()

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

    return pm, pl


def normal_force(body):
    # print(body)
    normals = body.cell_normals
    normal = sum(normals)
    center = body.center
    print(type(normal))
    if normal[2] < 0:
        normal *= -1

    p.add_mesh(pv.Line(center, (normal - center)))
    return center, normal


def moment_of_force(force, site_of_action):
    moment = np.array([- force[1] * site_of_action[2] + force[2] * site_of_action[1],
                       - force[2] * site_of_action[0] + force[0] * site_of_action[2],
                       - force[0] * site_of_action[1] + force[1] * site_of_action[0]])
    return moment


def result_of_forces_and_moments(force1, site_of_action1,
                                 force2=np.array([0, 0, 0]), site_of_action2=np.array([0, 0, 0]),
                                 force3=np.array([0, 0, 0]), site_of_action3=np.array([0, 0, 0]),
                                 force4=np.array([0, 0, 0]), site_of_action4=np.array([0, 0, 0]),
                                 force5=np.array([0, 0, 0]), site_of_action5=np.array([0, 0, 0]),
                                 force6=np.array([0, 0, 0]), site_of_action6=np.array([0, 0, 0]),
                                 force7=np.array([0, 0, 0]), site_of_action7=np.array([0, 0, 0]),
                                 force8=np.array([0, 0, 0]), site_of_action8=np.array([0, 0, 0]),
                                 force9=np.array([0, 0, 0]), site_of_action9=np.array([0, 0, 0]),
                                 force10=np.array([0, 0, 0]), site_of_action10=np.array([0, 0, 0])):
    force = force1 + force2 + force3 + force4 + force5 + force6 + force7 + force8 + force9 + force10

    moment1 = moment_of_force(force1, site_of_action1)
    moment2 = moment_of_force(force2, site_of_action2)
    moment3 = moment_of_force(force3, site_of_action3)
    moment4 = moment_of_force(force4, site_of_action4)
    moment5 = moment_of_force(force5, site_of_action5)
    moment6 = moment_of_force(force6, site_of_action6)
    moment7 = moment_of_force(force7, site_of_action7)
    moment8 = moment_of_force(force8, site_of_action8)
    moment9 = moment_of_force(force9, site_of_action9)
    moment10 = moment_of_force(force10, site_of_action10)

    moment = moment1 + moment2 + moment3 + moment4 + moment5 + moment6 + moment7 + moment8 + moment9 + moment10
    moment[0] = 0

    site_of_action = np.linalg.pinv(
        [[0, force[2], - force[1]], [- force[2], 0, force[0]], [force[1], - force[0], 0]]) * np.reshape(moment, (3, 1))

    return force, moment, site_of_action


def force_equilibrium():
    # ACL0 = 20
    ACL1 = np.array(tibia.points[2])
    ACL2 = np.array(flex.points[138])

    kACL = 10

    step_F = np.array([0.05, 0.05, 0.05])
    step_M = np.array([0.05, 0.05, 0.05])

    F_sign_old = np.array([0, 0, 0])
    M_sign_old = np.array([0, 0, 0])

    while True:
        ACL = ACL2 - ACL1
        ACL_length = np.linalg.norm(ACL)
        dACL_length = ACL_length - ACL0
        dACL = ACL * dACL_length / ACL_length

        F_ACL = - kACL * dACL
        F_lig = F_ACL

        # N = np.array([0, 0, -F_ACL[2]])
        # N = np.empty([1, 3])
        # poly_bodies = bodies.as_polydata_blocks
        # print(poly_bodies)
        # for i in poly_bodies.keys():
        #     N = np.append(N, normal_force(poly_bodies[i]))

        bodies, _, _ = contact_volume()
        center, normal = normal_force(bodies)
        N = - normal / normal[2] * F_lig[2]
        # print('F_lig = ', F_lig)
        # print('N = ', N)

        # F = F_ACL + N
        F, M, a = result_of_forces_and_moments(N, center, F_ACL, ACL2)

        F_length = np.linalg.norm(F)
        F_sign = np.sign(F)

        M_length = np.linalg.norm(M)
        M_sign = np.sign(M)

        for i in range(3):
            if np.any(F_sign[i] - F_sign_old[i]):
                step_F[i] /= 2

            if np.any(M_sign[i] - M_sign_old[i]):
                step_M[i] /= 2

        # print('step_F=', step_F)
        # print('step_M=', step_M)

        print('ACL=', ACL)
        # print('ACL_length=', ACL_length)
        # print('dACL_length=', dACL_length)
        print('dACL=', dACL)
        # print('F_ACL=', F_ACL)
        print('F_lig=', F_lig)
        print('N=', N)

        print('F=', F)
        print('F_sign=', F_sign)
        print('F_length=', F_length)

        print('M=', M)
        print('M_sign=', M_sign)
        print('M_length=', M_length)

        if F_length > 20:
            # for i in range(3):
            #     ACL2[i] -= F_sign[i] * step
            flex.transform(np.array([[1, 0, 0, F[0] * step_F[0]], [0, 1, 0, F[1] * step_F[1]],
                                     [0, 0, 1, F[2] * step_F[2]], [0, 0, 0, 1]]), inplace=True)
        #
        # if M_length > 10:
        #     flex.rotate_y(M[1] * step_M[1], inplace=True)
        #     flex.rotate_z(M[2] * step_M[2], inplace=True)

        else:
            break

        F_sign_old = F_sign

        # input()
    # p.add_mesh(pv.Line(ACL1, ACL2), color='r', line_width=2)


def update_scene():
    p1_1 = np.array(flex.points[14])
    p2_1 = np.array(flex.points[25])

    pm, pl = before_rotation()
    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)

    force_equilibrium()

    p1_2 = np.array(flex.points[14])
    p2_2 = np.array(flex.points[25])

    actual_axis_of_rotation(p1_1, p2_1, p1_2, p2_2)

    ACL1 = np.array(tibia.points[2])
    ACL2 = np.array(flex.points[138])

    p.add_mesh(pv.Line(ACL1, ACL2), color='r', line_width=2)

    p.update()


z_step = 0.02
fiy_step = 0.05
fi = 500
fi_step = 0.5
fi_max = int(140 / fi_step)

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

# ACL1 = np.array(tibia.points[2])
# ACL2 = np.array(flex.points[138])
ACL0 = np.linalg.norm(np.array(flex.points[138]) - np.array(tibia.points[2]))
print('ACL0=', ACL0)
# p.add_mesh(pv.Line(ACL1, ACL2), color='r', line_width=2)
# p.add_mesh(pv.Line(tibia.points[2], flex.points[138]), color='r', line_width=2)

print('Flexion')

cor0 = open(file0, 'a')
cor0.write(str('Flexion'))
cor0.write('\n')
cor0.close()

p.add_callback(update_scene, interval=200, count=fi_max)

p.show()
p.app.exec()
print('end')
