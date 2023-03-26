import pyvista as pv
import pandas as pd
import numpy as np
from pyvistaqt import BackgroundPlotter


fi_step = 0.5
fi_max = int(140 / fi_step)

p = pv.Plotter(window_size=(800, 1000))

p.camera.position = (-300, 0, -10)
p.camera.focal_point = (100, 0, -10)
axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
axes.origin = (0, 0, 0)
p.add_actor(axes.actor)

df = pd.read_csv('cor_empty.csv')
cor_empty = df.to_numpy()

for i in range(len(cor_empty)):
    pA = cor_empty[i, 0:3]
    pB = cor_empty[i, 3:6]

    line = pv.Line(pA, pB)
    p.add_mesh(line, color='g', line_width=2)

df = pd.read_csv('cor_1lig.csv')
cor_1lig = df.to_numpy()

for i in range(len(cor_1lig)):
    pA = cor_1lig[i, 0:3]
    pB = cor_1lig[i, 3:6]

    line = pv.Line(pA, pB)
    p.add_mesh(line, color='r', line_width=2)

df = pd.read_csv('cor_1lig_v2.csv')
cor_1lig_v2 = df.to_numpy()

for i in range(len(cor_1lig_v2)):
    pA = cor_1lig_v2[i, 0:3]
    pB = cor_1lig_v2[i, 3:6]

    line = pv.Line(pA, pB)
    p.add_mesh(line, color='b', line_width=2)

df = pd.read_csv('cor_slip.csv')
cor_slip = df.to_numpy()

for i in range(len(cor_slip)):
    pA = cor_slip[i, 0:3]
    pB = cor_slip[i, 3:6]

    line = pv.Line(pA, pB)
    p.add_mesh(line, color='y', line_width=2)

p.show()
