# Generate hex close packed cells (centers) in a sphere, containing a smaller spheroid (embolism)
# 
# Output: text file containing 4-tuples:
#  x y z cell_type
#

import numpy as np
#from fury import window, actor, ui
#import itertools
import math

#cell_radius = 1.0
cell_radius = 8.412710547954228  # PhysiCell default
xc = yc = -1.0

# setup hex packing constants
x_spacing = cell_radius*2
y_spacing = cell_radius*np.sqrt(3)

box_radius = 500.0
box_radius = 250.0
box_radius = 50.0
box_radius = 400.0
sphere_radius2 = box_radius * box_radius
eq_tri_yctr = math.tan(math.radians(30)) * cell_radius

# We'll append into these arrays
xyz = np.empty((0,3))
colors = np.empty((0,4))
	
# spheroid axes
a = 15
a2 = a*a
c = 9
c2 = c*c

# centroid of the emboli
x0_e = 200
y0_e = 50
y0_e = 10

fp = open("cells2d.dat","w")

z = 0.0
cell_type = 0
for y in np.arange(-box_radius, box_radius, y_spacing):
    yc += 1
    y2 = y
    ysq = y2 * y2
    term2 = (y2 - y0_e) * (y2 - y0_e)
    # print('--------')
    for x in np.arange(-box_radius, box_radius, x_spacing):
        x2 = x + (yc%2) * cell_radius 
        xsq = x2 * x2
        term1 = (x2 - x0_e) * (x2 - x0_e)
        if ( (xsq + ysq) < sphere_radius2):  # assume centered about origin
            xyz = np.append(xyz, np.array([[x2,y2,z]]), axis=0)
            # val = (xsq + ysq)/a2 + zsq/c2
            val = (term1 + term2)/a2 
            # print(val)
            # if val < 19.0:
            #     # colors = np.append(colors, np.array([[1,0,0, 1]]), axis=0)
            #     print('cell type 1')
            #     cell_type = 1
            # else:
            #     # colors = np.append(colors, np.array([[0,1,1, 1]]), axis=0)
            #     # colors = np.append(colors, np.array([[0,1,1,0.5]]), axis=0)
            #     cell_type = 0
            fp.write("%f,%f,%f,%d\n" % (x2,y2,z, cell_type))