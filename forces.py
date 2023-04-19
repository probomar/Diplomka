import tools as t
from setup import *


def normal_force():  # body):
    # normals = body.cell_normals()
    # normal = sum(normals)
    # center = body.center
    # if normal[2] < 0:
    #     normal *= -1
    #
    # p.add_mesh(pv.Line(center, (normal - center)))
    # return center, normal

    normal_vector_femur = np.array(flex.cell_normals)
    point_femur = np.array(femur.cell_centers().points)

    area_femur = flex.compute_cell_sizes(length=False, volume=False).cell_data["Area"]
    area_femur = area_femur.reshape([area_femur.shape[0], 1])

    N = np.empty([0, 3])

    for i in range(point_femur.shape[0]):
        pA = point_femur[i]
        pB = point_femur[i] + 200 * normal_vector_femur[i]
        points_tibia = tibia.ray_trace(pA, pB)[0]

        points_femoral_cartilage = flex_cartilage.ray_trace(pA, pB)[0]
        if np.shape(points_femoral_cartilage)[0] >= 2:
            femoral_cartilage_distance = np.linalg.norm(points_femoral_cartilage[0, :] - points_femoral_cartilage[1, :])
        else:
            femoral_cartilage_distance = 0

        points_tibial_cartilage = tibial_cartilage.ray_trace(pA, pB)[0]
        if np.shape(points_tibial_cartilage)[0] >= 2:
            tibial_cartilage_distance = np.linalg.norm(points_tibial_cartilage[0, :] - points_tibial_cartilage[1, :])
        else:
            tibial_cartilage_distance = 0

        cartilage_distance = femoral_cartilage_distance + tibial_cartilage_distance

        distance = np.empty([0])

        if not points_tibia.any():
            N = np.append(N, [[0, 0, 0]], axis=0)
        else:
            for j in range(points_tibia.shape[0]):
                distance = np.append(distance, np.linalg.norm(point_femur[i, :] - points_tibia[j, :]))

            min_distance = np.min(distance)

            if min_distance < cartilage_distance:
                N = np.append(N, [E * (min_distance - cartilage_distance) / cartilage_distance * area_femur[i]
                                  * normal_vector_femur[i]], axis=0)
                # line = pv.Line(point_femur[i], point_femur[i] - N[i])
                # p.add_mesh(line, color='r', line_width=2)
            else:
                N = np.append(N, [[0, 0, 0]], axis=0)

    N_forces = N.reshape([N.shape[0], 3])

    N = N_forces[0]
    soaN = point_femur[0]

    for i in range(N_forces.shape[0] - 1):
        N, MN, soaN = result_of_forces_and_moments(N, soaN, N_forces[i + 1], point_femur[i + 1])

    N_direction = N / np.linalg.norm(N)
    line = pv.Line(soaN, soaN - N)
    tip = pv.Cone(center=soaN - N_direction * 5, direction=N_direction, height=10, radius=2)
    p.add_mesh(line + tip, color='r', line_width=5, name='N')
    return N, soaN


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
    # print('force1=', force1)
    # print('force2=', force2)
    # print('force=', force)
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

    # site_of_action = np.linalg.pinv([[0, force[2], - force[1]], [- force[2], 0, force[0]], [force[1],
    #                                   - force[0], 0]]) * np.reshape(moment, (3, 1))
    # site_of_action = np.ravel(np.dot(np.linalg.pinv([[0, force[2], - force[1]], [- force[2], 0, force[0]],
    #                                                  [force[1], - force[0], 0]]), np.reshape(moment, (3, 1))))

    # print('moment=', moment)
    F = [[0, force[2], - force[1]], [- force[2], 0, force[0]], [force[1], - force[0], 0]]
    # print('F=', F)
    Ff = np.linalg.pinv(F)
    # print('Ff=', Ff)
    Mm = np.reshape(moment, (3, 1))
    # print('Mm=', Mm)
    X = np.dot(Ff, Mm)
    # print('X=', X)
    site_of_action = np.ravel(X)
    # print('site_of_site=', site_of_action)

    return force, moment, site_of_action


def ligament_force(lig0, lig1, lig2, klig, lig_name, lig_force_name):
    lig = lig2 - lig1
    lig_length = np.linalg.norm(lig)
    dlig_length = lig_length - lig0
    dlig = lig * dlig_length / lig_length

    if lig0 < lig_length:
        F_lig = - klig * dlig
    else:
        F_lig = np.array([0, 0, 0])
    p.add_mesh(pv.Line(lig1, lig2), color='b', line_width=2, name=lig_name)

    F_lig_direction = F_lig / np.linalg.norm(F_lig)
    line = pv.Line(lig2, lig2 - F_lig)
    tip = pv.Cone(center=lig2 - F_lig_direction * 5, direction=F_lig_direction, height=10, radius=2)
    p.add_mesh(line + tip, color='r', line_width=5, name=lig_force_name)

    return F_lig


def force_equilibrium():
    # print('ACL', ACL1, ACL2)

    step_F = np.array([0.05, 0.05, 0.05])
    step_M = np.array([0.05, 0.05, 0.05])

    F_sign_old = np.array([0, 0, 0])
    M_sign_old = np.array([0, 0, 0])

    while True:

        ACL1 = np.array(tibia.points[37])
        ACL2 = np.array(flex.points[190])

        PCL1 = np.array(tibia.points[24])
        PCL2 = np.array(flex.points[254])

        LCL1 = np.array(tibia.points[176])
        LCL2 = np.array(flex.points[200])

        MCL1 = np.array([49.8402, 34.2891, -35.3494])
        MCL2 = np.array(flex.points[102])

        F_ACL = ligament_force(ACL0, ACL1, ACL2, kACL, 'ACL', 'ACL_force')
        F_PCL = ligament_force(PCL0, PCL1, PCL2, kPCL, 'PCL', 'PCL_force')
        F_LCL = ligament_force(LCL0, LCL1, LCL2, kLCL, 'LCL', 'LCL_force')
        F_MCL = ligament_force(MCL0, MCL1, MCL2, kMCL, 'MCL', 'MCL_force')
        p.update()

        F_lig, M_lig, a_lig = result_of_forces_and_moments(F_ACL, ACL2, F_PCL, PCL2, F_LCL, LCL2, F_MCL, MCL2)

        # N = np.array([0, 0, -F_ACL[2]])
        # N = np.empty([1, 3])
        # poly_bodies = bodies.as_polydata_blocks
        # print(poly_bodies)
        # for i in poly_bodies.keys():
        #     N = np.append(N, normal_force(poly_bodies[i]))

        # bodies, _, _ = t.contact_volume()
        # center, normal = normal_force(bodies)
        # N = - normal / normal[2] * F_lig[2]
        # print('F_lig = ', F_lig)
        # print('N = ', N)

        N, center = normal_force()
        # print('N', N)
        # F = F_ACL + N
        F, M, a = result_of_forces_and_moments(N, center, F_lig, a_lig)

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

        # print('ACL=', ACL)
        # print('ACL_length=', ACL_length)
        # print('dACL_length=', dACL_length)
        # print('dACL=', dACL)
        # print('F_ACL=', F_ACL)
        print('F_lig=', F_lig)
        print('N=', N)

        print('F=', F)
        print('F_sign=', F_sign)
        print('F_length=', F_length)

        print('M=', M)
        print('M_sign=', M_sign)
        print('M_length=', M_length)

        if F_length > 10:
            # for i in range(3):
            #     ACL2[i] -= F_sign[i] * step
            F_transform = np.array([[1, 0, 0, F[0] * step_F[0]], [0, 1, 0, F[1] * step_F[1]],
                                    [0, 0, 1, F[2] * step_F[2]], [0, 0, 0, 1]])
            flex.transform(F_transform, inplace=True)
            flex_cartilage.transform(F_transform, inplace=True)
            # input()
        # if M_length > 10:
        #     y_rotate = M[1] * step_M[1]
        #     flex.rotate_y(y_rotate, inplace=True)
        #     flex_cartilage.rotate_y(y_rotate, inplace=True)
        #     z_rotate = M[2] * step_M[2]
        #     flex.rotate_z(z_rotate, inplace=True)
        #     flex_cartilage.rotate_z(z_rotate, inplace=True)

        else:
            break

        F_sign_old = F_sign
        p.update()

        # input()


def resultant_force(x, y, z):
    x0, y0, z0 = t.position0()
    transform = np.array([[1, 0, 0, x - x0], [0, 1, 0, y - y0], [0, 0, 1, z - z0], [0, 0, 0, 1]])
    flex.transform(transform)  # , inplace=True)
    flex_cartilage.transform(transform)  # , inplace=True)

    # ACL1 = np.array(tibia.points[37])
    # ACL2 = np.array(flex.points[190])
    #
    # PCL1 = np.array(tibia.points[144])
    # PCL2 = np.array(flex.points[254])
    #
    # MCL1 = np.array(tibia.points[176])
    # MCL2 = np.array(flex.points[200])
    #
    # LCL1 = np.array([49.8402, 34.2891, -35.3494])
    # LCL2 = np.array(flex.points[102])

    ACL1 = np.array(tibia.points[1074])
    ACL2 = np.array(flex.points[881])

    PCL1 = np.array(tibia.points[617])
    PCL2 = np.array(flex.points[1478])

    MCL1 = np.array(tibia.points[482])
    MCL2 = np.array(flex.points[1398])

    LCL1 = np.array([49.8402, 34.2891, -35.3494])
    LCL2 = np.array(flex.points[692])

    F_ACL = ligament_force(ACL0, ACL1, ACL2, kACL, 'ACL', 'ACL_force')
    F_PCL = ligament_force(PCL0, PCL1, PCL2, kPCL, 'PCL', 'PCL_force')
    F_LCL = ligament_force(LCL0, LCL1, LCL2, kLCL, 'LCL', 'LCL_force')
    F_MCL = ligament_force(MCL0, MCL1, MCL2,

                           kMCL, 'MCL', 'MCL_force')

    N, Nsoa = normal_force()

    force, moment, site_of_action = result_of_forces_and_moments(F_ACL, ACL2, F_PCL, PCL2, F_LCL, LCL2, F_MCL, MCL2,
                                                                 N, Nsoa)
    force_length = np.linalg.norm(force)
    moment[1] = 0
    moment_length = np.linalg.norm(moment)
    F_direction = force / np.linalg.norm(force)
    line = pv.Line(site_of_action, site_of_action - force)
    tip = pv.Cone(center=site_of_action - F_direction * 5, direction=F_direction, height=10, radius=2)
    p.add_mesh(line + tip, color='g', line_width=5, name='force')

    # return force_length
    return force, force_length, moment, moment_length, site_of_action
