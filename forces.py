import numpy as np
import tools as t
from setup import *


def normal_force(body):
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

        bodies, points_medial, points_lateral = t.contact_volume()

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

    normals = body.cell_normals()
    normal = sum(normals)
    center = body.center
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


def force_equilibrium(ACL0):
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

        if ACL0 < ACL_length:
            F_ACL = - kACL * dACL
        else:
            F_ACL = np.array([0, 0, 0])

        # F_ACL = - kACL * dACL

        F_lig = F_ACL

        # N = np.array([0, 0, -F_ACL[2]])
        # N = np.empty([1, 3])
        # poly_bodies = bodies.as_polydata_blocks
        # print(poly_bodies)
        # for i in poly_bodies.keys():
        #     N = np.append(N, normal_force(poly_bodies[i]))

        bodies, _, _ = t.contact_volume()
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
