import numpy as np
import forces as f
import tools as t
from setup import *
from matplotlib import pyplot as plt
import pandas as pd

p.add_mesh(flex, style='wireframe')
p.add_mesh(tibia, style='wireframe')
p.add_mesh(femoral_cartilage, style='wireframe')  # , color='b')
p.add_mesh(tibial_cartilage, style='wireframe')  # , color='b')


file1 = ['yzF0.csv', 'yzF10.csv', 'yzF20.csv', 'yzF30.csv', 'yzF40.csv', 'yzF50.csv', 'yzF60.csv','yzF70.csv',
         'yzF80.csv', 'yzF90.csv', 'yzF100.csv', 'yzF110.csv', 'yzF120.csv']
setup_fi = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
actual_fi = 0
stepz = 2
stepy = 2
rou = 1
sizey = 20
sizez = 10

for j in range(13):
    filex = file1[j]

    if os.path.exists(filex):
        os.remove(filex)

    F_value = [[None for k in range(sizey)] for l in range(sizez)]
    M_value = [[None for k in range(sizey)] for l in range(sizez)]
    y_values = [None] * sizey
    z_values = [None] * sizez
    i = 0

    x, y, z = t.position()
    roundx = round(x, 1)
    roundy = round(y, 1)
    roundz = round(z, 1)

    fi_rot = setup_fi[j] - actual_fi
    flex.rotate_vector(vector=[-1, 0, 0], angle=fi_rot, point=[0, 0, 0], inplace=True)
    flex_cartilage.rotate_vector(vector=[-1, 0, 0], angle=fi_rot, point=[0, 0, 0], inplace=True)
    actual_fi += fi_rot
    print('\n\nfi =', actual_fi)

    F_transform = np.array([[1, 0, 0, - x + roundx], [0, 1, 0, - y + roundy - sizey / 2 * stepy],
                            [0, 0, 1, - z + roundz - sizez / 2 * stepz], [0, 0, 0, 1]])
    flex.transform(F_transform, inplace=True)
    flex_cartilage.transform(F_transform, inplace=True)

    for y in range(sizey):
        for z in range(sizez):
            xa, ya, za = t.position()
            F, F_length, M, M_length, soa = f.resultant_force()

            yzF = pd.DataFrame(np.append(round(ya, rou), [round(za, rou), F_length, M_length]).reshape(1, 4))
            yzF.to_csv(filex, index=False, mode='a', header=False)

            print("{:<3} {:<3} {:<5} {:<20} {:<5} {:<20}".format(y, z, 'F =', F_length, 'M =', M_length))

            F_value[z][y] = F_length
            M_value[z][y] = M_length
            z_values[z] = round(za, rou)

            F_transform = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                                    [0, 0, 1, stepz], [0, 0, 0, 1]])
            flex.transform(F_transform, inplace=True)
            flex_cartilage.transform(F_transform, inplace=True)

            i += 1

        y_values[y] = round(ya, rou)
        F_transform = np.array([[1, 0, 0, 0], [0, 1, 0, stepy],
                                [0, 0, 1, -sizez * stepz], [0, 0, 0, 1]])
        flex.transform(F_transform, inplace=True)
        flex_cartilage.transform(F_transform, inplace=True)

    F_transform = np.array([[1, 0, 0, 0], [0, 1, 0, - sizey / 2 * stepy],
                            [0, 0, 1, - sizez / 2 * stepz + 15], [0, 0, 0, 1]])
    flex.transform(F_transform, inplace=True)
    flex_cartilage.transform(F_transform, inplace=True)

    plt.figure(j)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    im1 = ax1.imshow(F_value, cmap=viridis_r, interpolation='nearest')
    cb1 = plt.colorbar(im1)
    cb1.set_label('F')
    ax1.set_xticks(np.arange(sizey), labels=y_values, rotation=90)
    ax1.set_yticks(np.arange(sizez), labels=z_values)
    ax1.set_xlabel('y')
    ax1.set_ylabel('z')
    ax1.set_title('Force')
    im2 = ax2.imshow(M_value, cmap=viridis_r, interpolation='nearest')
    cb2 = plt.colorbar(im2)
    cb2.set_label('M')
    ax2.set_xticks(np.arange(sizey), labels=y_values, rotation=90)
    ax2.set_yticks(np.arange(sizez), labels=z_values)
    ax2.set_xlabel('y')
    ax2.set_ylabel('z')
    ax2.set_title('Moment')
    # fig.suptitle(filex)
    fig.suptitle('fi ='+str(setup_fi[j]))

plt.show()
