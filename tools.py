import pandas as pd
import math as m
import forces as f
from setup import *
import time as tim
# import pygad as pg
from scipy.optimize import minimize


def initialization():
    # contact_z()
    # max_fiy = max_contact_fiy(1)
    # min_fiy = max_contact_fiy(-1)
    # if max_fiy > min_fiy:
    #     contact_fiy_z(1)
    # else:
    #     contact_fiy_z(-1)
    #
    # cor0 = open(file0, 'a')
    # cor0.write(str('Flexion'))
    # cor0.write('\n')
    # cor0.close()
    # init_transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 20], [0, 0, 0, 1]])
    # flex.transform(init_transform, inplace=True)
    # flex_cartilage.transform(init_transform, inplace=True)

    # p.add_callback(
    f.force_equilibrium


def rotation_angle():
    global fi
    fi += fi_step
    print('fi =', fi)


def update_scene():
    start = tim.time()
    p1_1 = np.array(flex.points[14])
    p2_1 = np.array(flex.points[25])

    # slip_rotation()
    # t.rolling(tibia, flex)

    rotation_angle()

    rolling_with_ligament()

    p1_2 = np.array(flex.points[14])
    p2_2 = np.array(flex.points[25])

    actual_axis_of_rotation(p1_1, p2_1, p1_2, p2_2)

    p.update()
    end = tim.time()
    time = end - start
    print('time =', time)
    x = np.array(position())
    print('position =', x, '\n', '\n')


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


def rolling_with_ligament():
    pm, pl = before_rotation()
    flex.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)
    flex_cartilage.rotate_vector(vector=pm - pl, angle=fi_step, point=pm, inplace=True)
    f.force_equilibrium4()
    # optimize_position()
    # f.force_equilibrium(ACL0)

    # ACL1 = np.array(tibia.points[2])
    # ACL2 = np.array(flex.points[138])
    # p.add_mesh(pv.Line(ACL1, ACL2), color='r', line_width=2)


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


def contact_point():
    z = 0
    while True:
        collision, ncol = (tibia + tibial_cartilage).collision((flex + flex_cartilage), generate_scalars=True)
        # print('ncol=', ncol)
        if ncol != 0:
            break
        else:
            # print('z')
            transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]])
            flex.transform(transform)
            flex_cartilage.transform(transform)
            z -= z_step
            print('z=', z)

    contact_volumes = (tibia + tibial_cartilage).boolean_intersection(flex + flex_cartilage)
    # print(contact_volumes.n_cells)
    if contact_volumes.n_cells == 0:
        centr = np.array([0, 0, 0])
    else:
        threshed = contact_volumes.threshold()
        bodies = threshed.split_bodies()
        volume = np.empty((0, 1), int)
        center = np.empty((0, 3), int)
        for i, body in enumerate(bodies):
            volume = np.append(volume, body.volume)
            center = np.append(center, [np.array(body.center)], axis=0)
        # print('i=', i)
        ind = np.argmax(volume)
        centr = center[ind]
    # print('centr=', centr)
    return centr


def before_rotation():
    cor4 = open(file0, 'a')

    a = 0

    while True:
        z = 0
        fiy = 0
        while True:
            collision, ncol = (tibia + tibial_cartilage).collision(flex + flex_cartilage)

            if ncol == 0:
                print('z')
                transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]])
                flex.transform(transform)
                flex_cartilage.transform(transform)
                z -= z_step
            else:
                break

        bodies, points_medial, points_lateral = contact_volume()

        if (not points_medial.any()) and (a == 1):
            print('medial, z')
            transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]])
            flex.transform(transform)
            flex_cartilage.transform(transform)
            z -= z_step
            a = 0
        elif (not points_medial.any()) and (a != 1):
            print('medial')
            flex.rotate_y(- fiy_step, inplace=True)
            flex_cartilage.rotate_y(- fiy_step, inplace=True)
            fiy -= fiy_step
            a = -1
        elif (not points_lateral.any()) and (a == -1):
            print('lateral, z')
            transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -z_step], [0, 0, 0, 1]])
            flex.transform(transform)
            flex_cartilage.transform(transform)
            z -= z_step
            a = 0
        elif (not points_lateral.any()) and (a != -1):
            print('lateral')
            flex.rotate_y(fiy_step, inplace=True)
            flex_cartilage.rotate_y(fiy_step, inplace=True)
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
    contact_volumes = (tibia + tibial_cartilage).boolean_intersection(flex + flex_cartilage)
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


def function(paramt):
    x, y, z = paramt
    fun = f.resultant_force(x, y, z)
    return fun


def position():
    flex_position = flex.center
    # print(flex_position)
    x0 = flex_position[0]
    y0 = flex_position[1]
    z0 = flex_position[2]
    return x0, y0, z0


def fitness_func(solution, solution_idx):
    fitness = f.resultant_force(solution[0]/10, solution[1]/10, solution[2]/10)
    return fitness


def optimize_position():
    # ######## POKUS X0 = PUVODNI POLOHA  ######
    fun = lambda x: f.resultant_force(x[0], x[1], x[2])
    xf = np.array(position())
    # xp = np.array([0.000000001, 0.000001, 0.000001])
    x0 = xf  # + xp
    bnds = ((xf[0] - 2, xf[0] + 2), (xf[1] - 2, xf[1] + 2), (xf[2] - 2, xf[2] + 2))
    res = minimize(fun, x0, method='SLSQP', bounds=bnds, tol=1e-9, options={'disp': True})  # 'ftol': 1e-9,
    print('Vysledna poloha', res.x)

    # ############ POKUS VYCHYLENI FEMURU #############3
    # x0 = np.array([-100, 0, 0])
    # fun = lambda x: f.resultant_force(x[0], x[1], x[2])
    # res = minimize(fun, x0, method='SLSQP', options={'ftol': 1e-3, 'disp': True})
    # print('Vysledna poloha', res.x)

    # ##### POKUS GEN. ALG. ######    #
    # ga_instance = pg.GA(num_generations=50, num_parents_mating=2, fitness_func=fitness_func, sol_per_pop=10, num_genes=3,
    #                     gene_space=[range(-30, 10), range(20, 70), range(170, 220)])
    #                     # init_range_low=-5, init_range_high=25)
    # ga_instance.run()
    # solution, solution_fitness, solution_idx = ga_instance.best_solution()
    # print('Parameters of the best solution : {solution}'.format(solution=solution))
    # print('Fitness value of the best solution : {solution_fitness}'.format(solution_fitness=solution_fitness))

    # x0, y0, z0 = position0()
    transform = np.array([[1, 0, 0, res.x[0] - x0[0]], [0, 1, 0, res.x[1] - x0[1]], [0, 0, 1, res.x[2] - x0[2]], [0, 0, 0, 1]])
    flex.transform(transform)  # , inplace=True)
    flex_cartilage.transform(transform)  # , inplace=True)
