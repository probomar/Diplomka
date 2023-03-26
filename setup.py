import os
import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter


z_step = 0.02
fiy_step = 0.05
fi = 500
fi_step = 0.5
fi_max = int(120 / fi_step)

file0 = 'cor0.txt'
if os.path.exists(file0):
    os.remove(file0)

# file = 'cor_empty.csv'
# file = 'cor_slip.csv'
# file = 'cor_1lig.csv'
file = 'cor_1lig_v2.csv'

if os.path.exists(file):
    os.remove(file)

pv.global_theme.show_edges = True

femur = pv.read('models/femur_mini.stl')
tibia = pv.read('models/tibia_mini.stl')

flex = femur

p = BackgroundPlotter(window_size=(800, 1000))

p.camera.position = (-300, 0, -10)
p.camera.focal_point = (100, 0, -10)

axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
axes.origin = (0, 0, 0)
p.add_actor(axes.actor)

ACL0 = np.linalg.norm(np.array(flex.points[138]) - np.array(tibia.points[2]))
