import forces as f
import tools as t
from setup import *
from matplotlib import pyplot as plt
import pandas as pd
import time
import math


def angle(vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    ang = np.arccos(dot_product) * 180 / math.pi
    return ang


def force_equilibrium():
    step_F = 0.0001
    step_M = 0.00001
    alpha = 1.2
    beta = 0.8
    # step = 0.00001
    # F_old = 1000000
    # M_old = 1000000
    x, y, z = t.position()
    F_old, F_old_length, M_old, M_old_length, soa = f.resultant_force()
    i = 0

    while True:
        # # x, y, z = t.position0()
        F, F_length, M, M_length, soa = f.resultant_force()  # x, y, z)
        # # print("{:<3} {:<10} {:<25} {:<10} {:<25}".format('A', 'F length =', F_length, 'M length =', M_length))
        #
        F_M = pd.DataFrame(np.append(F_length, M_length).reshape(1, 2))
        F_M.to_csv(file1, index=False, mode='a', header=False)

        # if F_old < F_length:
        #     print('F:',  F_old, '<', F_length)
        #     step_F /= 2

        # if M_old < M_length:
        #     print('M:', M_old, '<', M_length)
        #     step_M /= 2

        # if ((F_old < F_length) & (F_length > 1)) or ((M_old < M_length) & (M_length > 1)):
        # if (((F_length - F_old) / F_length > 0.1) & (F_length > 1)) or\
        #         (((M_length - M_old) / M_length > 0.1) & (M_length > 1)):
        #     if (((F_length - F_old) / F_length > 0.1) & (F_length > 1)) &\
        #             (((M_length - M_old) / M_length > 0.1) & (M_length > 1)):
        #         print('F:',  F_old, '<', F_length, 'M:', M_old, '<', M_length)
        #     elif F_old < F_length:
        #         print('F:',  F_old, '<', F_length)
        #     elif M_old < M_length:
        #         print('M:', M_old, '<', M_length)
        #
        #     step /= 4
        #     step *= 3
        #     print('step =', step)
        #
        fiF = angle(F_old, F)
        print("{:<10} {:<25} {:<10} {:<25} {:<5} {:<15}".format
              ('F length =', F_length, 'F old =', F_old_length, 'fiF =', fiF))

        if (fiF < 10) & (abs((F_length - F_old_length) / F_length) < 0.1):
            step_F *= alpha
        elif fiF > 90:
            step_F *= beta
        print('step_F =', step_F)

        F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
                                [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
        # # F_transform = np.array([[1, 0, 0, 10 * F[0] * step], [0, 1, 0, 10 * F[1] * step],
        # #                         [0, 0, 1, 10 * F[2] * step], [0, 0, 0, 1]])
        flex.transform(F_transform, inplace=True)
        flex_cartilage.transform(F_transform, inplace=True)
        F_old = F
        F_old_length = F_length

        F, F_length, M, M_length, soa = f.resultant_force()
        # print("{:<3} {:<10} {:<25} {:<10} {:<25}".format('B', 'F length =', F_length, 'M length =', M_length))
        # print('M=', M)
        # print('M_old=', M_old)
        fiM = angle(M_old, M)
        print("{:<10} {:<25} {:<10} {:<25} {:<5} {:<15}".format
              ('M length =', M_length, 'M old =', M_old_length, 'fiM =', fiM))

        if (fiM < 20) & (abs((M_length - M_old_length) / M_length) < 0.1):
            step_M *= alpha
        elif fiM > 80:
            step_M *= beta
        print('step_M =', step_M)

        rotate_angle = M_length * step_M * 180 / math.pi
        # rotate_angle = M_length * step * 180 / math.pi
        flex.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)
        flex_cartilage.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)

        M_old = M
        M_old_length = M_length

        if (F_length < 1) & (M_length < 1):
            print('i =', i)
            break
        i += 1

    # step_F = 0.01
    # step_M = 0.00001
    #
    # while True:
    #     F_old = 1000000
    #     M_old = 1000000
    #
    #     while True:
    #         x, y, z = t.position0()
    #         F, F_length, M, M_length, soa = f.resultant_force(x, y, z)
    #         print("{:<10} {:<25} {:<10} {:<25}".format('F length =', F_length, 'M length =', M_length))
    #
    #         if F_old < F_length:
    #             print('F:', F_old, '<', F_length)
    #             step_F /= 2
    #
    #         F_transform = np.array([[1, 0, 0, F[0] * step_F], [0, 1, 0, F[1] * step_F],
    #                                 [0, 0, 1, F[2] * step_F], [0, 0, 0, 1]])
    #         flex.transform(F_transform, inplace=True)
    #         flex_cartilage.transform(F_transform, inplace=True)
    #
    #         F_old = F_length
    #
    #         if F_length < 1:
    #             break
    #
    #     while True:
    #         x, y, z = t.position0()
    #         F, F_length, M, M_length, soa = f.resultant_force(x, y, z)
    #         print("{:<10} {:<25} {:<10} {:<25}".format('F length =', F_length, 'M length =', M_length))
    #
    #         if M_old < M_length:
    #             print('M:', M_old, '<', M_length)
    #             step_M /= 2
    #
    #         rotate_angle = M_length * step_M * 180 / math.pi
    #         flex.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)
    #         flex_cartilage.rotate_vector(vector=M, angle=rotate_angle, point=soa, inplace=True)
    #
    #         M_old = M_length
    #
    #         if M_length < 1:
    #             break
    #
    #     if (F_length < 1) & (M_length < 1):
    #         break


start = time.time()

p.add_mesh(flex, style='wireframe')
p.add_mesh(tibia, style='wireframe')
p.add_mesh(femoral_cartilage, style='wireframe')  # , color='b')
p.add_mesh(tibial_cartilage, style='wireframe')  # , color='b')

x0 = np.array(t.position())
print(x0)

# file1 = 'xyzF.csv'
# if os.path.exists(file1):
#     os.remove(file1)
#
# # ########   POKUS F = fce(x, 0, 0)   ##########
# fun = lambda x: f.resultant_force(x[0], x[1], x[2])
# xes = np.arange(-4, 1, 0.5)
# yes = np.arange(2, 7, 0.5)
# zes = np.arange(17, 22, 0.5)
# xax = []
# yax = []
# zax = []
# outs = []
# i = 0
#
# for x in xes:
#     for y in yes:
#         start = time.time()
#         for z in zes:
#             xax.append(x)
#             yax.append(y)
#             zax.append(z)
#             F = fun([x, y, z])
#             outs.append(F)
#             xyzF = pd.DataFrame(np.append(x, [y, z, F]).reshape(1, 4))
#             xyzF.to_csv(file1, index=False, mode='a', header=False)
#         finish = time.time()
#         print('time=', finish - start)
#         i += 1
#         print(i)
#
# # df = pd.read_csv('xyzF.csv', header=None)
# # # print(df)
# #
# # data = df.to_numpy()
# # # print(data)
# #
# # xes = data[:, 0]
# # yes = data[:, 1]
# # zes = data[:, 2]
# # outs = data[:, 3]
# k = np.argmin(outs)
# print('MIn F =', outs[k])
# print('Min position =', xes[k], yes[k], zes[k])
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# img = ax.scatter(xes, yes, zes, c=outs, cmap='jet', alpha=1)
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# cbar = fig.colorbar(img)
# plt.show()

x0, y0, z0 = t.position()
x = x0
y = y0
z = z0  # + 10
transform = np.array([[1, 0, 0, x - x0], [0, 1, 0, y - y0], [0, 0, 1, z - z0], [0, 0, 0, 1]])
flex.transform(transform, inplace=True)
flex_cartilage.transform(transform, inplace=True)

# rotate_angle = 90
# flex.rotate_vector(vector=(-1, 0, 0), angle=rotate_angle, inplace=True)
# flex_cartilage.rotate_vector(vector=(-1, 0, 0), angle=rotate_angle, inplace=True)

# t.optimize_position()
force_equilibrium()

end = time.time()
time = end - start
print('time =', time)
x = np.array(t.position())
print('position =', x)

# x, y, z = res.x
# x0, y0, z0 = t.position0()
# transform = np.array([[1, 0, 0, x - x0], [0, 1, 0, y - y0], [0, 0, 1, z - z0], [0, 0, 0, 1]])
# flex.transform(transform, inplace=True)
# flex_cartilage.transform(transform, inplace=True)
# print(t.position0())
# print(f.resultant_force(x, y, z))

# t.initialization()
# p.add_callback(t.update_scene, interval=200, count=fi_max)
# p.add_callback(f.force_equilibrium)  # , interval=200, count=fi_max)

p.show()
p.app.exec()
