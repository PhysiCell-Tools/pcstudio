#
# anim_pressure.py:  render/animate PhysiCell .svg files, using left/right arrows on keyboard
#
# Usage:
#  python anim_pressure.py <start_index axes_min axes_max>
#    i.e., the arguments <...> are optional and have defaults.
# 
# Keyboard arrows: right/left arrows will single step forward/backward; up/down will increment/decrement step size
#
# Dependencies include matplotlib and numpy. We recommend installing the Anaconda Python3 distribution.
#
# Examples (run from directory containing the .svg files):
#  python anim_pressure.py 
#  python anim_pressure.py 5 700 1300 
#
# Author: Randy Heiland (except for the circles() function)
#
#
__author__ = "Randy Heiland"

import sys
import glob
import os
import xml.etree.ElementTree as ET
import math
from pyMCDS import pyMCDS
join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"
try:
  import matplotlib
  import matplotlib.colors as mplc
  from matplotlib.patches import Circle, Ellipse, Rectangle
  from matplotlib.collections import PatchCollection
  from matplotlib.colors import BoundaryNorm
  from matplotlib.ticker import MaxNLocator
  from matplotlib import colors as mcolors
except:
  print("\n---Error: cannot import matplotlib")
  print("---Try: python -m pip install matplotlib")
  print(join_our_list)
#  print("---Consider installing Anaconda's Python 3 distribution.\n")
  raise
try:
  import numpy as np  # if mpl was installed, numpy should have been too.
except:
  print("\n---Error: cannot import numpy")
  print("---Try: python -m pip install numpy\n")
  print(join_our_list)
  raise
from collections import deque
try:
  # apparently we need mpl's Qt backend to do keypresses 
#  matplotlib.use("Qt5Agg")
  matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
except:
  print("\n---Error: cannot use matplotlib's TkAgg backend")
  print(join_our_list)
#  print("Consider installing Anaconda's Python 3 distribution.")
  raise


current_idx = 0
print("# args=",len(sys.argv)-1)

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
axes_min = 0.0
axes_max = 1000  # but overridden by "width" attribute in .svg
if (len(sys.argv) == 5):
  use_defaults = False
  kdx = 1
#  show_nucleus = int(sys.argv[kdx])
#  kdx += 1
  current_idx = int(sys.argv[kdx])
  kdx += 1
  axes_min = float(sys.argv[kdx])
  kdx += 1
  axes_max = float(sys.argv[kdx])
elif (len(sys.argv) != 1):
  print("Please provide either no args or 4 args:")
  usage_str = "start_index axes_min axes_max"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 0 2000" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)

#"""
#print("show_nucleus=",show_nucleus)
print("current_idx=",current_idx)
print("axes_min=",axes_min)
print("axes_max=",axes_max)
#"""

"""
if (len(sys.argv) > 1):
   current_idx = int(sys.argv[1])
if (len(sys.argv) > 2):
   axes_min = float(sys.argv[2])
   axes_max = float(sys.argv[3])

if (len(sys.argv) > 4):
  usage_str = "[<start_index> [<axes_min axes_max>]]"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 1 10 700 1300" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)
"""

print("current_idx=",current_idx)

#d={}   # dictionary to hold all (x,y) positions of cells

""" 
--- for example ---
In [141]: d['cell1599'][0:3]
Out[141]: 
array([[ 4900.  ,  4900.  ],
       [ 4934.17,  4487.91],
       [ 4960.75,  4148.02]])
"""

fig = plt.figure(figsize=(9,7))
ax = fig.gca()
#ax.set_aspect("equal")


#plt.ion()

time_delay = 0.1

cbar = None

count = -1
#while True:

#-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    """
    See https://gist.github.com/syrte/592a062c562cd2a98a83 

    Make a scatter plot of circles. 
    Similar to plt.scatter, but the size of circles are in data scale.
    Parameters
    ----------
    x, y : scalar or array_like, shape (n, )
        Input data
    s : scalar or array_like, shape (n, ) 
        Radius of circles.
    c : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs.
        Note that `c` should not be a single numeric RGB or RGBA sequence 
        because that is indistinguishable from an array of values
        to be colormapped. (If you insist, use `color` instead.)  
        `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
    vmin, vmax : scalar, optional, default: None
        `vmin` and `vmax` are used in conjunction with `norm` to normalize
        luminance data.  If either are `None`, the min and max of the
        color array is used.
    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
        norm, cmap, transform, etc.
    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`
    Examples
    --------
    a = np.arange(11)
    circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
    plt.colorbar()
    License
    --------
    This code is under [The BSD 3-Clause License]
    (http://opensource.org/licenses/BSD-3-Clause)
    """

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    # if c is not None:
    #     try:
    #         print("------ in circles(): calling plt.sci(collection) ----------")
    #         plt.sci(collection)
    #     except:
    #         print("------ ERROR in circles(): calling plt.sci(collection) ----------")
    return collection

#-----------------------------------------------------
def plot_pressure():
  global current_idx, axes_max, cbar
#   fname = "snapshot%08d.svg" % current_idx
  fname = "output%08d.xml" % current_idx
  print("--------- plot_pressure(): fname = ",fname)

#   if (os.path.isfile(fname) == False):
#     print("File does not exist: ",fname)
#     return


  mcds = pyMCDS(fname, '../tmpdir', microenv=False, graph=False, verbose=True)
  total_min = mcds.get_time()
  print("    time=",total_min)
  cell_pressure = mcds.get_cell_df()['pressure']
  num_cells = len(cell_pressure)
  print("  len(cell_pressure) = ",len(cell_pressure))
  vmin = cell_pressure.min()
  vmax = cell_pressure.max()
  fix_cmap = 0
  print(f'   cell_pressure.min(), max() = {cell_pressure.min()}, {cell_pressure.max()}')
  cell_vol = mcds.get_cell_df()['total_volume']
  print(f'   cell_vol.min(), max() = {cell_vol.min()}, {cell_vol.max()}')

    # static double four_thirds_pi =  4.188790204786391;
  four_thirds_pi =  4.188790204786391
    # radius = phenotype.volume.total;
    # radius /= four_thirds_pi;
    # radius = pow( radius , 0.333333333333333333333333333333333333333 );
  cell_radii = np.divide(cell_vol, four_thirds_pi)
  cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

  xvals = mcds.get_cell_df()['position_x']
  yvals = mcds.get_cell_df()['position_y']
#   zvals = mcds.get_cell_df()['position_z']

#   xlist = deque()
#   ylist = deque()
#   rlist = deque()
#   rgb_list = deque()

#  print('\n---- ' + fname + ':')
#   tree = ET.parse(fname)
#   root = tree.getroot()
#  print('--- root.tag ---')
#  print(root.tag)
#  print('--- root.attrib ---')
#  print(root.attrib)

  title_str = "(" + str(current_idx) + ") Current time: " + str(total_min) + "m"
  title_str += " (" + str(num_cells) + " agents)"
#   axes_min = -1000.
#   axes_max = -axes_min
  axes_min = mcds.get_mesh()[0][0][0][0]
  axes_max = mcds.get_mesh()[0][0][-1][0]

#   for icell in range(len(cell_pressure)):
    #   if icell < 5:
    #       print(f'{icell}) {cell_pressure[icell]}')

    #   if (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
    #     rgb = list(map(int, s[4:-1].split(","))) 
    #     rgb[:]=[x/255. for x in rgb]
    #   else:     # otherwise, must be a color name
    #     rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
    #     rgb = [x for x in rgb_tuple]

#   rgbs =  np.array(rgb_list)

#  print('type(rgbs) = ',type(rgbs))
#  print('rgbs = ',rgbs)

  plt.cla()
  plt.title(title_str)
  plt.xlim(axes_min,axes_max)
  plt.ylim(axes_min,axes_max)

#   circles(xvals,yvals, s=rvals, color=rgbs)
#   circles(xvals,yvals, s=rvals, color=rgbs)
#   circles(xvals,yvals, s=2)
#   facecolors = [cm.jet(x) for x in np.random.rand(num_cells)]
#   facecolors = [plt.cm.viridis(x) for x in np.random.rand(num_cells)]
#   print("facecolors=",facecolors)
#   cvals = np.random.rand(num_cells)
#   my_plot = circles(xvals,yvals, s=cell_radii, color="white", edgecolor='black', linewidth=0.5)
#   my_plot = circles(xvals,yvals, s=cell_radii, facecolors=facecolors, edgecolor='black', linewidth=0.5)
  print(" -- calling circles(): c=",cell_pressure)
  my_plot = circles(xvals,yvals, s=cell_radii, c=cell_pressure, edgecolor='black', linewidth=0.5)

#   cmap = plt.cm.hot
  if True:
    num_contours = 10
#    vmin = 30.
#    vmax = 38.

#     levels = MaxNLocator(nbins=30).tick_values(vmin, vmax)
# #    cmap = plt.get_cmap('PiYG')
#     cmap = plt.get_cmap('viridis')
#     norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#    my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), num_contours, cmap='viridis') #'viridis'
    if fix_cmap > 0:
      # my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), levels=levels, cmap=cmap)
    #   my_plot = plt.contourf(xgrid, ygrid, M[field_idx, :].reshape(numy, numx, ), levels=levels, extend='both', cmap=cmap)
        pass
    else:
      # my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), cmap=cmap)
    #   my_plot = plt.contourf(xgrid, ygrid, M[field_idx, :].reshape(numy, numx), cmap=cmap)
        pass

    if cbar == None:  # if we always do this, it creates an additional colorbar!
#      cbar = plt.colorbar(my_plot, boundaries=np.arange(vmin, vmax, 1.0))
      cbar = plt.colorbar(my_plot)
      print("cbar=",cbar)
    else:
      cbar.ax.clear()
      cbar = plt.colorbar(my_plot, cax=cbar.ax)
      print("cbar(2)=",cbar)

#plt.xlim(0,2000)  # TODO - get these values from width,height in .svg at top
#plt.ylim(0,2000)
  plt.pause(time_delay)

step_value = 1
def press(event):
  global current_idx, step_value
#    print('press', event.key)
  sys.stdout.flush()
  if event.key == 'escape':
    sys.exit(1)
  elif event.key == 'h':  # help
    print('esc: quit')
    print('right arrow: increment by step_value')
    print('left arrow:  decrement by step_value')
    print('up arrow:   increment step_value by 1')
    print('down arrow: decrement step_value by 1')
    print('0: reset to 0th frame')
    print('h: help')
  elif event.key == 'left':  # left arrow key
#    print('go backwards')
#    fig.canvas.draw()
    current_idx -= step_value
    if (current_idx < 0):
      current_idx = 0
    plot_pressure()
  elif event.key == 'right':  # right arrow key
#        print('go forwards')
#        fig.canvas.draw()
    current_idx += step_value
    plot_pressure()
  elif event.key == 'up':  # up arrow key
    step_value += 1
    print('step_value=',step_value)
  elif event.key == 'down':  # down arrow key
    step_value -= 1
    if (step_value <= 0):
      step_value = 1
    print('step_value=',step_value)
  elif event.key == '0':  # reset to 0th frame/file
    current_idx = 0
    plot_pressure()
  else:
    print('press', event.key)


#for current_idx in range(40):
#  fname = "snapshot%08d.svg" % current_idx
#  plot_pressure(fname)
plot_pressure()
print("\nNOTE: click in plot window to give it focus before using keys.")

fig.canvas.mpl_connect('key_press_event', press)

# keep last plot displayed
#plt.ioff()
plt.show()
