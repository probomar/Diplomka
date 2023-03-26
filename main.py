import tools as t
from setup import *


t.initialization()

p.add_mesh(flex, style='wireframe')
p.add_mesh(tibia, style='wireframe')

p.add_callback(t.update_scene, interval=200, count=fi_max)

p.show()
p.app.exec()
