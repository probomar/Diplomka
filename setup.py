
import os
import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter
# import pygap as pg

z_step = 0.02
fiy_step = 0.05
fi = 500
fi_step = 0.5
fi_max = int(120 / fi_step)
E = 10.35  # MPa
kACL = 10
kPCL = 10
kLCL = 10
kMCL = 10

ACL0 = 18
PCL0 = 30
LCL0 = 50
MCL0 = 30

file0 = 'cor0.txt'
if os.path.exists(file0):
    os.remove(file0)

# file = 'cor_empty.csv'
# file = 'cor_slip.csv'
# file = 'cor_1lig.csv'
file = 'cor_1lig_v2.csv'

if os.path.exists(file):
    os.remove(file)

file1 = 'F_M6.csv'

if os.path.exists(file1):
    os.remove(file1)

pv.global_theme.show_edges = True

femur = pv.read('models/femur.stl')
tibia = pv.read('models/tibia.stl')
femoral_cartilage = pv.read('models/femoral_cartilage.stl')
tibial_cartilage = pv.read('models/lateral_tibial_cartilage.stl') \
                   + pv.read('models/medial_tibial_cartilage.stl')

# femur = pv.read('models/femur_mini.stl')
# tibia = pv.read('models/tibia_mini.stl')
# femoral_cartilage = pv.read('models/femoral_cartilage_mini.stl')
# tibial_cartilage = pv.read('models/lateral_tibial_cartilage_mini.stl') \
#                    + pv.read('models/medial_tibial_cartilage_mini.stl')


flex = femur
flex_cartilage = femoral_cartilage
full_flex = flex + flex_cartilage
full_tibia = tibia + tibial_cartilage

# print('ACL=', np.linalg.norm(np.array(flex.points[190]) - np.array(tibia.points[37])))
# print('PCL=', np.linalg.norm(np.array(flex.points[254]) - np.array(tibia.points[144])))
# print('LCL=', np.linalg.norm(np.array(flex.points[200]) - np.array(tibia.points[176])))
# print('MCL=', np.linalg.norm(np.array(flex.points[102]) - np.array([49.8402, 34.2891, -35.3494])))
# input()

p = BackgroundPlotter(window_size=(800, 1000))

p.camera.position = (-300, 0, -10)
p.camera.focal_point = (100, 0, -10)

axes = pv.Axes(show_actor=True, actor_scale=50, line_width=5)
axes.origin = (0, 0, 0)
# p.add_actor(axes.actor)
