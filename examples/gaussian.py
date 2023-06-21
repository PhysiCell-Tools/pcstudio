import sys
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from scipy.stats import norm

yscale = float(sys.argv[1])

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
    if c is not None:
        plt.sci(collection)
    return collection
    #-------------------------------------------

mean = 0
std_dev = 20

# x_values = np.arange(-50, 50, 0.2)
xmin = -50
xmax = -xmin
x_values = np.arange(xmin, xmax, 1)
y_values = norm(mean, std_dev)
# plt.plot(x_values, y_values.pdf(x_values))
yv = y_values.pdf(x_values) * yscale
print(yv.min(),yv.max())
plt.plot(x_values, yv)

print(x_values)
print(yv)

# y_values = norm(mean, 2)
# plt.plot(x_values, y_values.pdf(x_values))
# y_values = norm(mean, 4)
# plt.plot(x_values, y_values.pdf(x_values))
# yv = y_values.pdf(x_values)
# print(yv.min(),yv.max())

# plt.plot(x_values, yv*50,'--')

#ax.set_title('Normal Gaussian Curve')

cell_radius = 1.  # ~2 micron spacing
cell_radius = 2.5 # ~5 micron spacing of subcells; Area=19.63
cell_diam = cell_radius*2

x_min = -50.0
x_max = -x_min
y_min = 0.0
y_max = 20

#yc = -1.0
y_idx = -1
# hex packing constants
x_spacing = cell_radius*2
y_spacing = cell_radius*np.sqrt(3)

cells_x = np.array([])
cells_y = np.array([])

y_idx = 0
for yval in np.arange(y_min,y_max, y_spacing):
    y_idx += 1
    for xval in np.arange(x_min,x_max, x_spacing):
        xval_offset = xval + (y_idx%2) * cell_radius
        ixval = int(xval_offset)
        # print(ixval)
        idx = np.where(x_values == ixval)
        if yval < yv[idx]:
        # if (xval >= xvals[kdx]) and (xval <= xvals[kdx+1]):
            cells_x = np.append(cells_x, xval_offset)
            cells_y = np.append(cells_y, yval)
            print(xval_offset,',',yval,',0.0, 2, 101')  # x,y,z, cell type, [sub]cell ID
            # plt.plot(xval_offset,yval,'ro',markersize=30)

circles(cells_x,cells_y, s=cell_radius, c='b', ec='black', linewidth=0.1)

plt.show()
