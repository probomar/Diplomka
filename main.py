import numpy as np

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

print('fi =', fi)
f.force_equilibrium4()

end = time.time()
time = end - start
print('time =', time)
x = np.array(t.position())
print('position =', x)


p.add_callback(t.update_scene, interval=200, count=fi_max)

p.show()
p.app.exec()
