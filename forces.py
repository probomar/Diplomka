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


def moment_of_force(force, site_of_action, point=np.array([0, 0, 0])):
    if force.all() == 0:
        moment = np.array([0, 0, 0])
    else:
        param = ((point - site_of_action @ force)) / (force @ force)
        # print(- site_of_action @ force)
        # print(force @ force)
        # print('t=', param)
        arm = site_of_action + force * param - point
        # print('R=', arm)
        moment = np.array([- force[1] * arm[2] + force[2] * arm[1],
                           - force[2] * arm[0] + force[0] * arm[2],
                           - force[0] * arm[1] + force[1] * arm[0]])
    # print('M=', moment)

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

    F = [[0, force[2], - force[1]], [- force[2], 0, force[0]], [force[1], - force[0], 0]]
    Ff = np.linalg.pinv(F)
    Mm = np.reshape(moment, (3, 1))
    X = np.dot(Ff, Mm)
    site_of_action = np.ravel(X)

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
    # # print('ACL', ACL1, ACL2)
    #
    # step_F = np.array([0.05, 0.05, 0.05])
    # step_M = np.array([0.05, 0.05, 0.05])
    #
    # F_sign_old = np.array([0, 0, 0])
    # M_sign_old = np.array([0, 0, 0])
    #
    # while True:
    #
    #     ACL1 = np.array(tibia.points[37])
    #     ACL2 = np.array(flex.points[190])
    #
    #     PCL1 = np.array(tibia.points[24])
    #     PCL2 = np.array(flex.points[254])
    #
    #     LCL1 = np.array(tibia.points[176])
    #     LCL2 = np.array(flex.points[200])
    #
    #     MCL1 = np.array([49.8402, 34.2891, -35.3494])
    #     MCL2 = np.array(flex.points[102])
    #
    #     F_ACL = ligament_force(ACL0, ACL1, ACL2, kACL, 'ACL', 'ACL_force')
    #     F_PCL = ligament_force(PCL0, PCL1, PCL2, kPCL, 'PCL', 'PCL_force')
    #     F_LCL = ligament_force(LCL0, LCL1, LCL2, kLCL, 'LCL', 'LCL_force')
    #     F_MCL = ligament_force(MCL0, MCL1, MCL2, kMCL, 'MCL', 'MCL_force')
    #     p.update()
    #
    #     F_lig, M_lig, a_lig = result_of_forces_and_moments(F_ACL, ACL2, F_PCL, PCL2, F_LCL, LCL2, F_MCL, MCL2)
    #
    #     # N = np.array([0, 0, -F_ACL[2]])
    #     # N = np.empty([1, 3])
    #     # poly_bodies = bodies.as_polydata_blocks
    #     # print(poly_bodies)
    #     # for i in poly_bodies.keys():
    #     #     N = np.append(N, normal_force(poly_bodies[i]))
    #
    #     # bodies, _, _ = t.contact_volume()
    #     # center, normal = normal_force(bodies)
    #     # N = - normal / normal[2] * F_lig[2]
    #     # print('F_lig = ', F_lig)
    #     # print('N = ', N)
    #
    #     N, center = normal_force()
    #     # print('N', N)
    #     # F = F_ACL + N
    #     F, M, a = result_of_forces_and_moments(N, center, F_lig, a_lig)
    #
    #     F_length = np.linalg.norm(F)
    #     F_sign = np.sign(F)
    #
    #     M_length = np.linalg.norm(M)
    #     M_sign = np.sign(M)
    #
    #     for i in range(3):
    #         if np.any(F_sign[i] - F_sign_old[i]):
    #             step_F[i] /= 2
    #
    #         if np.any(M_sign[i] - M_sign_old[i]):
    #             step_M[i] /= 2
    #
    #     # print('step_F=', step_F)
    #     # print('step_M=', step_M)
    #
    #     # print('ACL=', ACL)
    #     # print('ACL_length=', ACL_length)
    #     # print('dACL_length=', dACL_length)
    #     # print('dACL=', dACL)
    #     # print('F_ACL=', F_ACL)
    #     print('F_lig=', F_lig)
    #     print('N=', N)
    #
    #     print('F=', F)
    #     print('F_sign=', F_sign)
    #     print('F_length=', F_length)
    #
    #     print('M=', M)
    #     print('M_sign=', M_sign)
    #     print('M_length=', M_length)
    #
    #     if F_length > 10:
    #         # for i in range(3):
    #         #     ACL2[i] -= F_sign[i] * step
    #         F_transform = np.array([[1, 0, 0, F[0] * step_F[0]], [0, 1, 0, F[1] * step_F[1]],
    #                                 [0, 0, 1, F[2] * step_F[2]], [0, 0, 0, 1]])
    #         flex.transform(F_transform, inplace=True)
    #         flex_cartilage.transform(F_transform, inplace=True)
    #         # input()
    #     # if M_length > 10:
    #     #     y_rotate = M[1] * step_M[1]
    #     #     flex.rotate_y(y_rotate, inplace=True)
    #     #     flex_cartilage.rotate_y(y_rotate, inplace=True)
    #     #     z_rotate = M[2] * step_M[2]
    #     #     flex.rotate_z(z_rotate, inplace=True)
    #     #     flex_cartilage.rotate_z(z_rotate, inplace=True)
    #
    #     else:
    #         break
    #
    #     F_sign_old = F_sign
    #     p.update()
    #
    #     # input()

    step_F = 0.0001
    step_M = 0.00001
    alpha = 1.1
    beta = 1 / 1.1
    F, F_length, M, M_length, soa = resultant_force()
    print("{:<3} {:<10} {:<20} {:<10} {:<20}".format(' ', 'F length =', F_length, 'M length =', M_length))
    F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
    F_M.to_csv(file1, index=False, mode='a', header=False)
    i = 0
    j = []
    k = 0
    while True:
        l = 0
        m = 0
        while True:
            l += 1
            # print('l =', l)

            # print("{:<3} {:<15} {:<20} {:<15} {:<20}".format('A', 'F length =', F_length, 'M length =', M_length))

            # fiF = angle(F_old, F)
            # print("{:<10} {:<25} {:<10} {:<25} {:<5} {:<15}".format
            #       ('F length =', F_length, 'F old =', F_old_length, 'fiF =', fiF))
            #
            # if (fiF < 10) & (abs((F_length - F_old_length) / F_length) < 0.1):
            #     step_F *= alpha
            # elif fiF > 90:
            #     step_F *= beta
            # print('step_F =', step_F)

            F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
                                    [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
            flex.transform(F_transform, inplace=True)
            flex_cartilage.transform(F_transform, inplace=True)

            # F_old = F
            # F_old_length = F_length
            F_new, F_length_new, M_new, M_length_new, soa_new = resultant_force()
            # print("{:<3} {:<15} {:<20} {:<15} {:<20}".format('A', 'F length_new =', F_length_new, 'M length_new =',
            #                                                  M_length_new))

            if (F_length_new > 1 * F_length) or (M_length_new > 1.3 * M_length):
                # print('beta')
                F_transform = np.array([[1, 0, 0, - F[0] * step_F], [0, 1, 0, - F[1] * step_F],
                                        [0, 0, 1, - F[2] * step_F], [0, 0, 0, 1]])
                flex.transform(F_transform, inplace=True)
                flex_cartilage.transform(F_transform, inplace=True)
                step_F *= beta
                # print('step_F =', step_F)
                if l == 5:
                    k += 1
                    break
            else:
                # print('alpha')
                step_F *= alpha
                F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
                print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('A', 'F length =', F_length, 'M length =', M_length))
                F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
                F_M.to_csv(file1, index=False, mode='a', header=False)
                k = 0
                break

        j = np.append(j, l)
        # print('j =', j)

        while True:
            m += 1
            # print('m =', m)

            # print("{:<3} {:<15} {:<20} {:<15} {:<20}".format('B', 'F length =', F_length, 'M length =', M_length))

            # fiM = angle(M_old, M)
            # print("{:<10} {:<25} {:<10} {:<25} {:<5} {:<15}".format
            #       ('M length =', M_length, 'M old =', M_old_length, 'fiM =', fiM))
            #
            # if (fiM < 20) & (abs((M_length - M_old_length) / M_length) < 0.1):
            #     step_M *= alpha
            # elif fiM > 80:
            #     step_M *= beta
            # print('step_M =', step_M)

            rotate_angle = M_length * step_M * 180 / math.pi
            flex.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)
            flex_cartilage.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)

            # M_old = M
            # M_old_length = M_length

            F_new, F_length_new, M_new, M_length_new, soa_new = resultant_force()
            # print("{:<3} {:<15} {:<20} {:<15} {:<20}".format('B', 'F length_new =', F_length_new, 'M length_new =',
            #                                                  M_length_new))

            if (M_length_new > 1 * M_length) or (F_length_new > 1.3 * F_length):
                # print('beta')
                flex.rotate_vector(vector=M, angle=-rotate_angle, point=soa, inplace=True)
                flex_cartilage.rotate_vector(vector=M, angle=-rotate_angle, point=soa, inplace=True)
                step_M *= beta
                if m == 5:
                    k += 1
                    break
            else:
                # print('alpha')
                step_M *= alpha
                F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
                print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('B', 'F length =', F_length, 'M length =', M_length))
                F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
                F_M.to_csv(file1, index=False, mode='a', header=False)
                k = 0
                break

            # print('step_M =', step_M)

        j = np.append(j, m)
        # print('j =', j)

        i += 1
        # print('i =', i)
        # print('k =', k)
        if ((F_length < 1) & (M_length < 1)) or (k > 5) or (i > 100):
            print('\ni =', i, '\n')
            break


def force_equilibrium2():
    step_F = 0.00001
    step_M = 0.000001
    alpha = 1.1
    beta = 1 / 1.1
    F, F_length, M, M_length, soa = resultant_force()
    # center = t.contact_point()
    center = np.array([0, 0, 0])
    M = moment_of_force(F, soa, center)
    M_length = np.linalg.norm(M)
    print("{:<3} {:<10} {:<20} {:<10} {:<20}".format(' ', 'F length =', F_length, 'M length =', M_length))
    F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
    F_M.to_csv(file1, index=False, mode='a', header=False)
    i = 0
    j = []
    k = 0
    while True:
        l = 0
        m = 0
        while True:
            l += 1

            F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
                                    [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
            flex.transform(F_transform, inplace=True)
            flex_cartilage.transform(F_transform, inplace=True)

            F_new, F_length_new, M_new, M_length_new, soa_new = resultant_force()
            # center = t.contact_point()
            center = np.array([0, 0, 0])
            M_new = moment_of_force(F_new, soa_new, center)
            M_length_new = np.linalg.norm(M_new)
            if (F_length_new > 1 * F_length) or (M_length_new > 1.3 * M_length):
                F_transform = np.array([[1, 0, 0, - F[0] * step_F], [0, 1, 0, - F[1] * step_F],
                                        [0, 0, 1, - F[2] * step_F], [0, 0, 0, 1]])
                flex.transform(F_transform, inplace=True)
                flex_cartilage.transform(F_transform, inplace=True)
                step_F *= beta
                print("{:<3} {:<10}".format('A', 'Nic'))

                if l == 5:
                    k += 1
                    break
            else:
                step_F *= alpha
                F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
                print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('A', 'F length =', F_length, 'M length =', M_length))
                F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
                F_M.to_csv(file1, index=False, mode='a', header=False)
                k = 0
                break

        j = np.append(j, l)

        while True:
            m += 1
            rotate_angle = M_length * step_M * 180 / math.pi
            flex.rotate_vector(vector=M, angle=rotate_angle, point=center, inplace=True)
            flex_cartilage.rotate_vector(vector=M, angle=rotate_angle, point=center, inplace=True)

            F_new, F_length_new, M_new, M_length_new, soa_new = resultant_force()
            # print(M_length_new)
            # center = t.contact_point()
            center = np.array([0, 0, 0])
            M_new = moment_of_force(F_new, soa_new, center)
            M_length_new = np.linalg.norm(M_new)
            if (M_length_new > 1 * M_length) or (F_length_new > 1.3 * F_length):
                flex.rotate_vector(vector=M, angle=-rotate_angle, point=center, inplace=True)
                flex_cartilage.rotate_vector(vector=M, angle=-rotate_angle, point=center, inplace=True)
                step_M *= beta
                print("{:<3} {:<10}".format('B', 'Nic'))
                if m == 5:
                    k += 1
                    break
            else:
                step_M *= alpha
                F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
                print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('B', 'F length =', F_length, 'M length =', M_length))
                F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
                F_M.to_csv(file1, index=False, mode='a', header=False)
                k = 0
                break

        j = np.append(j, m)
        i += 1

        if ((F_length < 1) & (M_length < 1)) or (k > 5) or (i > 100):
            print('\ni =', i, '\n')
            break


def force_equilibrium3():
    step_F = 0.00005
    step_M = 0.000002
    F_old, F_length_old, M_old, M_length_old, soa_old = resultant_force()
    # center = t.contact_point()
    center = np.array([0, 0, 0])
    M_old = moment_of_force(F_old, soa_old, center)
    M_length_old = np.linalg.norm(M_old)
    print("{:<3} {:<10} {:<20} {:<10} {:<20}".format(' ', 'F length =', F_length_old, 'M length =', M_length_old))

    F_M = pd.DataFrame(np.append(F_length_old, M_length_old).reshape(1, 2))
    F_M.to_csv(file1, index=False, mode='a', header=False)
    F, F_length, M, M_length, soa = F_old, F_length_old, M_old, M_length_old, soa_old

    while True:
        F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
                                [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
        flex.transform(F_transform, inplace=True)
        flex_cartilage.transform(F_transform, inplace=True)

        F, F_length, M, M_length, soa = resultant_force()
        # center = t.contact_point()
        center = np.array([0, 0, 0])
        M = moment_of_force(F, soa, center)
        M_length = np.linalg.norm(M)
        print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('A ', 'F length =', F_length, 'M length =', M_length))

        F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
        F_M.to_csv(file1, index=False, mode='a', header=False)

        rotate_angle = M_length * step_M * 180 / math.pi
        flex.rotate_vector(vector=M, angle=rotate_angle, point=center, inplace=True)
        flex_cartilage.rotate_vector(vector=M, angle=rotate_angle, point=center, inplace=True)

        F, F_length, M, M_length, soa = resultant_force()
        # center = t.contact_point()
        center = np.array([0, 0, 0])
        M = moment_of_force(F, soa, center)
        M_length = np.linalg.norm(M)
        print("{:<3} {:<10} {:<20} {:<10} {:<20}".format('B ', 'F length =', F_length, 'M length =', M_length))

        F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
        F_M.to_csv(file1, index=False, mode='a', header=False)

        if (F_length < 0.25 * F_length_old) & (M_length < 0.25 * M_length_old):
            break


def force_equilibrium4():
    step_F = 0.002
    alpha = 1.1
    beta = 1 / 1.5

    F_old, F_length_old, M_old, M_length_old, soa_old = resultant_force()
    # center = t.contact_point()
    center = np.array([0, 0, 0])
    M_old = moment_of_force(F_old, soa_old, center)
    M_length_old = np.linalg.norm(M_old)
    print("{:<7} {:<10} {:<20} {:<10} {:<20}".format(' ', 'F length =', F_length_old, 'M length =', M_length_old))

    F_M = pd.DataFrame(np.append(F_length_old, M_length_old).reshape(1, 2))
    F_M.to_csv(file1, index=False, mode='a', header=False)
    F, F_length, M, M_length, soa = F_old, F_length_old, M_old, M_length_old, soa_old
    i = 0
    while True:
        F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
                                [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
        flex.transform(F_transform, inplace=True)
        flex_cartilage.transform(F_transform, inplace=True)

        F_new, F_length_new, M_new, M_length_new, soa_new = resultant_force()
        # center = t.contact_point()
        center = np.array([0, 0, 0])
        M_new = moment_of_force(F_new, soa_new, center)
        M_length_new = np.linalg.norm(M)

        if 0.95 * F_length > F_length_new:
            step_F *= alpha
            F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
            print("{:<7} {:<10} {:<20} {:<10} {:<20}".format('alpha', 'F length =', F_length, 'M length =', M_length))
            F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
            F_M.to_csv(file1, index=False, mode='a', header=False)

        elif 1.05 * F_length < F_length_new:
            F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
            print("{:<7} {:<10} {:<20} {:<10} {:<20}".format('beta', 'F length =', F_length, 'M length =',
                                                             M_length))
            # F_transform = np.array([[1, 0, 0, - F[0] * step_F], [0, 1, 0, - F[1] * step_F],
            #                         [0, 0, 1, - F[2] * step_F], [0, 0, 0, 1]])
            # flex.transform(F_transform, inplace=True)
            # flex_cartilage.transform(F_transform, inplace=True)
            step_F *= beta
            F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
            F_M.to_csv(file1, index=False, mode='a', header=False)

        else:
            F, F_length, M, M_length, soa = F_new, F_length_new, M_new, M_length_new, soa_new
            print("{:<7} {:<10} {:<20} {:<10} {:<20}".format(' ', 'F length =', F_length, 'M length =', M_length))
            F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
            F_M.to_csv(file1, index=False, mode='a', header=False)

        i += 1
        if (F_length < 1) or ((i > 100) & (F_length < 0.10 * F_length_old)):
            break

    print('i =', i, '\n')


def resultant_force():  # x, y, z):
    # x0, y0, z0 = t.position0()
    # transform = np.array([[1, 0, 0, x - x0], [0, 1, 0, y - y0], [0, 0, 1, z - z0], [0, 0, 0, 1]])
    # flex.transform(transform)  # , inplace=True)
    # flex_cartilage.transform(transform)  # , inplace=True)

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

    LCL1 = np.array([54.0785, -5.56702, -48.8082])
    LCL2 = np.array(flex.points[692])

    F_ACL = ligament_force(ACL0, ACL1, ACL2, kACL, 'ACL', 'ACL_force')
    F_PCL = ligament_force(PCL0, PCL1, PCL2, kPCL, 'PCL', 'PCL_force')
    F_LCL = ligament_force(LCL0, LCL1, LCL2, kLCL, 'LCL', 'LCL_force')
    F_MCL = ligament_force(MCL0, MCL1, MCL2, kMCL, 'MCL', 'MCL_force')

    N, Nsoa = normal_force()

    force, moment, site_of_action = result_of_forces_and_moments(F_ACL, ACL2, F_PCL, PCL2, F_LCL, LCL2, F_MCL, MCL2,
                                                                 N, Nsoa)
    force_length = np.linalg.norm(force)
    moment_length = np.linalg.norm(moment)
    F_direction = force / np.linalg.norm(force)
    line = pv.Line(site_of_action, site_of_action - force)
    tip = pv.Cone(center=site_of_action - F_direction * 5, direction=F_direction, height=10, radius=2)
    p.add_mesh(line + tip, color='g', line_width=5, name='force')

    return force, force_length, moment, moment_length, site_of_action
