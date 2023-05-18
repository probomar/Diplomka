import pyvista as pv
import pandas as pd
import numpy as np
from pyvistaqt import BackgroundPlotter
import matplotlib.pyplot as plt


# fi_step = 0.5
# fi_max = int(140 / fi_step)
#
# p = pv.Plotter(window_size=(800, 1000))
#
# p.camera.position = (-300, 0, -10)
# p.camera.focal_point = (100, 0, -10)
# axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
# axes.origin = (0, 0, 0)
# p.add_actor(axes.actor)
#
# df = pd.read_csv('cor_empty.csv')
# cor_empty = df.to_numpy()
#
# for i in range(len(cor_empty)):
#     pA = cor_empty[i, 0:3]
#     pB = cor_empty[i, 3:6]
#
#     line = pv.Line(pA, pB)
#     p.add_mesh(line, color='g', line_width=2)
#
# df = pd.read_csv('cor_1lig.csv')
# cor_1lig = df.to_numpy()
#
# for i in range(len(cor_1lig)):
#     pA = cor_1lig[i, 0:3]
#     pB = cor_1lig[i, 3:6]
#
#     line = pv.Line(pA, pB)
#     p.add_mesh(line, color='r', line_width=2)
#
# df = pd.read_csv('cor_1lig_v2.csv')
# cor_1lig_v2 = df.to_numpy()
#
# for i in range(len(cor_1lig_v2)):
#     pA = cor_1lig_v2[i, 0:3]
#     pB = cor_1lig_v2[i, 3:6]
#
#     line = pv.Line(pA, pB)
#     p.add_mesh(line, color='b', line_width=2)
#
# df = pd.read_csv('cor_slip.csv')
# cor_slip = df.to_numpy()
#
# for i in range(len(cor_slip)):
#     pA = cor_slip[i, 0:3]
#     pB = cor_slip[i, 3:6]
#
#     line = pv.Line(pA, pB)
#     p.add_mesh(line, color='y', line_width=2)
#
# p.show()


def read_data(file):
    df = pd.read_csv(file)
    F_M = df.to_numpy()
    F = np.empty(len(F_M))
    M = np.empty(len(F_M))
    x = range(len(F_M))

    for i in x:
        F[i] = F_M[i, 0]
        M[i] = F_M[i, 1]

    return F, M, x


F1, M1, x1 = read_data('F_M1.csv')
F2, M2, x2 = read_data('F_M2.csv')
F3, M3, x3 = read_data('F_M3.csv')
F4, M4, x4 = read_data('F_M4.csv')
F5, M5, x5 = read_data('F_M5.csv')
F6, M6, x6 = read_data('F_M6.csv')
F7, M7, x7 = read_data('F_M7.csv')
F8, M8, x8 = read_data('F_M8.csv')
F9, M9, x9 = read_data('F_M9.csv')

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
plt.suptitle('Constant step')
plt.subplot(2, 1, 1)
# plt.plot(x1, F1, label='step = 0.0001')
# plt.plot(x2, F2, label='step = 0.00005')
# plt.plot(x3, F3, label='step = 0.00002')
# plt.plot(x4, F4, label='step = 0.00001')
# plt.plot(x5, F5, label='step_F = 0.0001, step_M = 0.00001')
plt.plot(x6, F6, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.05, beta = 1/1.05, 1.3')
plt.plot(x7, F7, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.05, beta = 1/1.05, 1.2')
plt.plot(x8, F8, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.1, beta = 1/1.1, 1.3')
plt.plot(x9, F9, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.15, beta = 1/1.15, 1.3')

# plt.plot([0, 4107], [1, 1], label='condition')
# plt.xlabel('iteration')
plt.ylabel('F [N]')
plt.legend()

plt.subplot(2, 1, 2)
# plt.plot(x1, M1, label='step = 0.0001')
# plt.plot(x2, M2, label='step = 0.00005')
# plt.plot(x3, M3, label='step = 0.00002')
# plt.plot(x4, M4, label='step = 0.00001')
# plt.plot(x5, M5, label='step_F = 0.0001, step_M = 0.00001')
plt.plot(x6, M6, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.05, beta = 1/1.05, 1.3')
plt.plot(x7, M7, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.05, beta = 1/1.05, 1.2')
plt.plot(x8, M8, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.1, beta = 1/1.1, 1.3')
plt.plot(x9, M9, label=' step_F = 0.0001, step_M = 0.00001, alpha = 1.15, beta = 1/1.15, 1.3')

# plt.plot([0, 4107], [1, 1], label='condition')
plt.xlabel('iteration')
plt.ylabel('M [Nmm]')
plt.show()






