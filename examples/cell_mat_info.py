import sys
import numpy as np
import scipy.io
from pyMCDS_cells import pyMCDS_cells

xml_file = sys.argv[1]

mcds = pyMCDS_cells(xml_file, '.')  
# mcds = pyMCDS_cells(xml_file, 'tmpdir')  
print('time=', mcds.get_time())

print(mcds.data['discrete_cells'].keys())

ncells = len(mcds.data['discrete_cells']['ID'])
print('total_volume= ',mcds.data['discrete_cells']['total_volume'])
print('ncells=', ncells)

# global xyz
xyz = np.zeros((ncells, 3))
xyz[:, 0] = mcds.data['discrete_cells']['position_x']
xyz[:, 1] = mcds.data['discrete_cells']['position_y']
xyz[:, 2] = mcds.data['discrete_cells']['position_z']
#xyz = xyz[:1000]
# print("position_x = ",xyz[:,0])
xmin = min(xyz[:,0])
xmax = max(xyz[:,0])
print("xmin = ",xmin)
print("xmax = ",xmax)

ymin = min(xyz[:,1])
ymax = max(xyz[:,1])
print("ymin = ",ymin)
print("ymax = ",ymax)

zmin = min(xyz[:,2])
zmax = max(xyz[:,2])
print("zmin = ",zmin)
print("zmax = ",zmax)

cell_type = mcds.data['discrete_cells']['cell_type']
# print(type(cell_type))
# print(cell_type)
unique_cell_type = np.unique(cell_type)
print("\nunique_cell_type = ",unique_cell_type )
