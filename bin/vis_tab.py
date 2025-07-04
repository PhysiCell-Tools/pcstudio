"""
vis_tab.py - provide visualization on Plot tab. Cells can be plotted on top of substrates/signals.

Authors:
Randy Heiland (heiland@iu.edu),
Daniel Bergman, Vincent Noel, Heber Rocha, Marco Ruscone,
Dr. Paul Macklin (macklinp@iu.edu)
Rf. Credits.md
"""

# import traceback
import sys
import os
import time
# import inspect
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
from pathlib import Path

from vis_base import VisBase
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.colors as mplc
import cmaps
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from matplotlib import gridspec
from collections import deque
import glob
import csv
import pandas

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame,QWidget,QCheckBox,QComboBox,QVBoxLayout,QLabel,QMessageBox
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRectF, Qt
locale_en_US = QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates)

import numpy as np
import scipy.io
from pyMCDS_cells import pyMCDS_cells 
from pyMCDS import pyMCDS
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

#-----------------------------
#   Future idea of floating Plot window
class MainPlotWindow(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel("Plot")
        # self.layout.addWidget(self.label)

        self.figure = plt.figure()
        # self.canvas = FigureCanvasQTAgg(self.figure)
        # self.canvas.setStyleSheet("background-color:transparent;")
        # self.ax0 = self.figure.add_subplot(111, adjustable='box')
        # self.layout.addWidget(self.canvas)
        self.layout.addWidget(canvas)

        # self.close_button = QPushButton("Close")
        # self.close_button.setStyleSheet("background-color: lightgreen;")
        # # self.close_button.setFixedWidth(150)
        # self.close_button.clicked.connect(self.close_plot_cb)
        # self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        # self.hide()
        # self.show()

#---------------------------------------------------------------
class Vis(VisBase, QWidget):

    def __init__(self, studio_flag, rules_flag, nanohub_flag, config_tab, microenv_tab, celldef_tab, user_params_tab, rules_tab, ics_tab, run_tab, model3D_flag, tensor_flag, ecm_flag, galaxy_flag):

        super(Vis,self).__init__(studio_flag=studio_flag, rules_flag=rules_flag,  nanohub_flag=nanohub_flag, config_tab=config_tab, microenv_tab=microenv_tab, celldef_tab=celldef_tab, user_params_tab=user_params_tab, rules_tab=rules_tab, ics_tab=ics_tab, run_tab=run_tab, model3D_flag=model3D_flag,tensor_flag=tensor_flag, ecm_flag=ecm_flag, galaxy_flag=galaxy_flag)

        self.figure = None

        # self.vis2D = True
        # self.model3D_flag = model3D_flag
        # self.tensor_flag = tensor_flag

        self.circle_radius = 100  # will be set in run_tab.py using the .xml
        self.mech_voxel_size = 30

        # self.nanohub_flag = nanohub_flag
        # self.run_tab = run_tab
        # self.legend_tab = None

        self.bgcolor = [1,1,1,1]  # all 1.0 for white 

        # self.population_plot = None
        self.celltype_name = []
        self.celltype_color = []
        self.discrete_variable = None

        self.animating_flag = False

        self.xml_root = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.play_plot_cb)

        self.fix_cmap_flag = False
        # self.cells_edge_checked_flag = True
        self.cell_edge = True
        self.cell_fill = True
        self.cell_line_width = 0.5
        self.cell_line_width2 = 0.8
        self.cell_alpha = 0.5

        self.num_contours = 50
        # self.shading_choice = 'auto'  # 'auto'(was 'flat') vs. 'gouraud' (smooth)
        self.shading_choice = 'gouraud'  # 'auto'(was 'flat') vs. 'gouraud' (smooth)

        self.fontsize = 7
        self.label_fontsize = 6
        self.cbar_label_fontsize = 8
        self.title_fontsize = 10

        self.plot_cells_svg = True

        self.cell_scalars_l = []

        self.field_index = 4  # substrate (0th -> 4 in the .mat)
        self.substrate_name = None

        self.plot_xmin = None
        self.plot_xmax = None
        self.plot_ymin = None
        self.plot_ymax = None

        self.axes_x_center = 0
        self.axes_y_center = 0
        self.axes_x_radius = 100
        self.axes_y_radius = 100

        self.use_defaults = True
        self.title_str = ""

        self.show_plot_range = False

        # self.config_file = "mymodel.xml"
        self.physiboss_node_dict = {}
        
        self.reset_model_flag = True
        self.x_range = self.xmax - self.xmin

        self.y_range = self.ymax - self.ymin

        self.aspect_ratio = 0.7

        self.view_aspect_square = True
        # self.view_smooth_shading = False

        self.show_voxel_grid = False
        self.show_mechanics_grid = False
        self.show_vectors = False

        self.show_edge = True
        self.show_nucleus = False
        self.alpha = 0.7

        basic_length = 12.0
        self.figsize_width_substrate = 15.0  # allow extra for colormap(s)
        self.figsize_height_substrate = basic_length

        self.cax1 = None
        self.cax2 = None

        self.figsize_width_2Dplot = basic_length
        self.figsize_height_2Dplot = basic_length

        # self.width_substrate = basic_length  # allow extra for colormap
        # self.height_substrate = basic_length

        self.figsize_width_svg = basic_length
        self.figsize_height_svg = basic_length


        # self.output_dir = "/Users/heiland/dev/PhysiCell_V.1.8.0_release/output"
        # self.output_dir = "output"
        # self.output_dir = "../tmpdir"   # for nanoHUB
        # self.output_dir = "tmpdir"   # for nanoHUB

        # temporary debugging plotting without having to Run first
        # if self.nanohub_flag:
        #     self.output_dir = "."   # for nanoHUB
        # else:
        #     self.output_dir = "tmpdir"

        # stop the insanity!
        self.output_dir = "."   # for nanoHUB  (overwritten in studio.py, based on config_tab)
        # self.output_dir = "tmpdir"   # for nanoHUB

        #-------------------------------------------
        label_width = 110
        value_width = 60
        label_height = 20
        units_width = 70

        # Beware: padding seems to alter the behavior; adding scroll arrows to choices list!
                # padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px;
                # height: 30px;
            # QComboBox{
            #     color: #000000;
            #     background-color: #FFFFFF; 
            #     height: 20px;
            # }
            # QComboBox:disabled {
            #     background-color: rgb(199,199,199);
            #     color: rgb(99,99,99);
            # }
        self.stylesheet = """ 
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; } 
            QPushButton:hover { border: 1px solid; border-radius: 3px; border-color: rgb(33, 77, 115); } QPushButton:focus { outline-color: transparent; border: 2px solid; border-color: rgb(151, 195, 243); } QPushButton:pressed{ background-color: rgb(145, 255, 145); } 
            QPushButton:disabled { color: black; border-color: grey; background-color: rgb(199,199,199); }

            """
            # QPushButton{ font-family: "Segoe UI"; font-size: 8pt; border: 1px solid; border-color: rgb(46, 103, 156); border-radius: 3px; padding-right: 10px; padding-left: 10px; padding-top: 5px; padding-bottom: 5px; background-color: rgb(77, 138, 201); color: white; font: bold; width: 64px; } 
            # QPushButton{
            #     color:#000000;
            #     background-color: lightgreen; 
            #     border-style: outset;
            #     border-color: black;
            #     padding: 2px;
            # }
            # QLineEdit:disabled {
            #     background-color: rgb(199,199,199);
            #     color: rgb(99,99,99);
            # }
            # QPushButton:disabled {
            #     background-color: rgb(199,199,199);
            # }
                # color: #000000;
                # background-color: #FFFFFF; 
                # border-style: outset;
                # border-width: 2px;
                # border-radius: 10px;
                # border-color: beige;
                # font: bold 14px;
                # min-width: 10em;
                # padding: 6px;
                # padding: 1px 18px 1px 3px;

        # Need to have the substrates_combobox before doing create_figure!
        self.canvas = None
        self.create_figure()
        self.scroll_plot.setWidget(self.canvas) # for an embedded Plot window (not floating)

        # -- future idea of [optional] floating Plot window
        # self.plot_win = None
        # self.plot_win = MainPlotWindow(self.canvas)
        # self.plot_win.show()

        # self.plot_w.setWidget(self.canvas) # self.config_params = QWidget()

    #--------------------------------------
    # def aspect_11_cb(self,bval):
    #     print("vis_tab: aspect_11_cb()  self.aspect_11_checkbox.isChecked()= ",self.aspect_11_checkbox.isChecked())
    #     # self.vis_tab.aspect_11_cb(self.aspect_11_checkbox.isChecked())
    #     # self.view_aspect_square = bval
    #     self.view_aspect_toggle_cb(bval)


    #--------------------------------------
    def write_cells_csv_cb(self):
        print("vis_tab.py: write_cells_csv_cb")

        xml_file_root = "output%08d.xml" % self.current_frame
        xml_file = os.path.join(self.output_dir, xml_file_root)
        # xml_file = os.path.join("tmpdir", xml_file_root)  # temporary hack

        if not Path(xml_file).is_file():
            print("ERROR: file not found",xml_file)
            return

        mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
        # total_min = mcds.get_time()  # warning: can return float that's epsilon from integer value
    
        xvals = mcds.get_cell_df()['position_x']
        # print("type(xvals)= ",type(xvals))
        yvals = mcds.get_cell_df()['position_y']
        cell_types = mcds.get_cell_df()["cell_type"]
        # print("len(xvals)=",len(xvals))
        # print("x,y,z,type,volume,cycle entry,custom:GFP,custom:sample")
        self.get_cell_types_from_config()
        # print("self.celltype_name=",self.celltype_name)
        csv_file = open("snap.csv", "w")
        csv_file.write("x,y,z,type,volume,cycle entry,custom:GFP,custom:sample\n")
        try:
            for xv, yv, ct in zip(xvals, yvals, cell_types):  # DON'T do sequential idx
                # print(f'{xv},{yv},{self.celltype_name[int(ct)]}')
                csv_file.write(f'{xv},{yv},0.0,{self.celltype_name[int(ct)]}\n')
        except:
            print("\nvis_tab.py:-------- Error writing snap.csv file")
        csv_file.close()

    #--------------------------------------
    def reset_axes_cb(self):
        # print("vis_tab.py: reset_axes_cb")
        # self.axes_x_center, axes_y_center, axes_x_radius, axes_y_radius, 
        self.plot_xmin = self.axes_x_center - self.axes_x_radius
        self.plot_xmax = self.axes_x_center + self.axes_x_radius

        self.plot_ymin = self.axes_y_center - self.axes_y_radius
        self.plot_ymax = self.axes_y_center + self.axes_y_radius
        self.update_plots()

    #--------------------------------------
    # Dependent on 2D/3D
    def update_plots(self):
        # print("------ vis_tab.py: update_plots()")
        # for line in traceback.format_stack():
        #     print(line.strip())
        self.ax0.cla()
        if self.substrates_checked_flag:  # do first so cells are plotted on top
            self.plot_substrate(self.current_frame)
        
        if self.graph_display_type != 'NONE':
            self.build_attachments(self.current_frame)
        
        if self.cells_checked_flag:
            if self.plot_cells_svg:
                self.plot_svg(self.current_frame)
            elif self.physiboss_vis_flag:
                self.plot_cell_physiboss(self.current_frame)
            else:
                self.plot_cell_scalar(self.current_frame)

            if self.graph_display_type != 'NONE':
                df_cells = self.get_current_cells_df()
                if df_cells is not None:
                    xvals = df_cells['position_x']
                    yvals = df_cells['position_y']
                    for c1,c2 in self.attachments:
                        self.ax0.plot([xvals[c1], xvals[c2]], [yvals[c1], yvals[c2]], 'k-', lw=0.5)

        # show grid(s), but only if Cells or Substrates checked?
        if self.show_voxel_grid:
            self.plot_voxel_grid()
        if self.show_mechanics_grid:
            self.plot_mechanics_grid()

        self.called_from_update = True
        self.frame_count.setText(str(self.current_frame))
        self.called_from_update = False

        self.canvas.update()
        self.canvas.draw()

        if self.save_frame:
            self.frame_ind += 1
            frame_file = os.path.join(self.output_dir, f"frame{self.frame_ind:04d}{self.save_frame_filetype}")
            print("---->  ", frame_file)
            self.figure.savefig(frame_file)

    def get_mcds_cells_df(self, mcds):
        try:
            df_all_cells = mcds.get_cell_df()
        except:
            print("vis_tab.py: plot_cell_scalar(): error performing mcds.get_cell_df()")
            return
        if self.celltype_filter:
            return df_all_cells.loc[ df_all_cells['cell_type'].isin(self.celltype_filter) ]
        else:
            return df_all_cells

    def get_current_cells_df(self):
        xml_file_root = "output%08d.xml" % self.current_frame
        xml_file = os.path.join(self.output_dir, xml_file_root)
        if not Path(xml_file).is_file():
            print("ERROR: file not found", xml_file)
            return None
        mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
        return self.get_mcds_cells_df(mcds)

    #------------------------------
    # Depends on 2D/3D
    def create_figure(self):
        print("\n--   vis_tab.py: --------- create_figure(): ------- creating figure, canvas, ax0")
        if self.figure is not None:
            print("              self.figure is None, so return!")
            return
        self.figure = plt.figure()
        self.gs = gridspec.GridSpec(2,2, height_ratios=[20,1], width_ratios=[20,1]) # top row is [plot, substrate colorbar]; bottom row is [cells colorbar, nothing]
        self.canvas = FigureCanvasQTAgg(self.figure)
        print("     self.canvas= ",self.canvas)
        self.canvas.setStyleSheet("background-color:transparent;")

        # Adding one subplot for image
        # self.ax0 = self.figure.add_subplot(111)
        # self.ax0 = self.figure.add_subplot(111, adjustable='box', aspect=1.2)
        # self.ax0 = self.figure.add_subplot(111, adjustable='box', aspect=self.aspect_ratio)
        self.ax0 = self.figure.add_subplot(self.gs[0,0], adjustable='box')
        
        # self.ax0.get_xaxis().set_visible(False)
        # self.ax0.get_yaxis().set_visible(False)
        # plt.tight_layout()

        self.reset_model()

    def build_attachments(self, frame):
        if self.graph_display_type == 'neighbors':
            fname = "output%08d_cell_neighbor_graph.txt" % frame
        elif self.graph_display_type == 'attachments':
                fname = "output%08d_attached_cells_graph.txt" % frame
        elif self.graph_display_type == 'spring attachments':
            fname = "output%08d_spring_attached_cells_graph.txt" % frame
        else:
            print("vis_tab.py: build_attachments(): ERROR: graph_display_type not set to neighbors, attachments, or spring attachments")
            return
        path = os.path.join(self.output_dir, fname)
        self.attachments = set()

        if Path(path).is_file():
            with open(path, 'r') as attachments_file:
                for line in attachments_file.readlines()[1:]:
                    cell, atts = line.split(":")
                    if len(atts.strip()) > 0:
                        for att in atts.split(","):
                            self.attachments.add(tuple(sorted([int(cell), int(att.strip())])))
            
    #------------------------------------------------------------
    # not currently used, but maybe useful
    def plot_vecs(self):
        # global current_frame

        fname = "output%08d.xml" % self.current_frame
        # print("plot_vecs(): fname = ",fname)
        # full_fname = os.path.join(self.output_dir, fname)
        # mcds=pyMCDS_cells("output00000049.xml")
        try:
            # mcds = pyMCDS_cells(fname)
            # print("plot_vecs(): self.output_dir= ",self.output_dir)
            mcds = pyMCDS_cells(fname, self.output_dir)
            # print(mcds.get_cell_variables())

            xpos = mcds.data['discrete_cells']['position_x']
            ypos = mcds.data['discrete_cells']['position_y']
            # print("------- plot_vecs(): xpos=", xpos)

            xvec = mcds.data['discrete_cells']['xvec']
            yvec = mcds.data['discrete_cells']['yvec']
            # # print("------- plot_vecs(): xvals=", mcds.data['discrete_cells']['position_x'])
            # # print("------- plot_vecs(): yvals=", mcds.data['discrete_cells']['position_y'])
            # # print("------- plot_vecs(): xvec=", mcds.data['discrete_cells']['xvec'])
            # # print("------- plot_vecs(): yvec=", mcds.data['discrete_cells']['yvec'])

            # # lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
            sfact = 30
            vlines = []
            for idx in range(len(xpos)):
                x0 = xpos[idx]
                y0 = ypos[idx]
                x1 = xpos[idx] + xvec[idx]*sfact
                y1 = ypos[idx] + yvec[idx]*sfact
                vlines.append( [(x0,y0), (x1,y1)] )
            # print("vlines = ",vlines)
            # ax = plt.gca()
            self.line_collection = LineCollection(vlines, color="black", linewidths=0.5)
            self.ax0.add_collection(self.line_collection)
        except:
            print("plot_vecs(): ERROR")
            pass

    #------------------------------------------------------------
    # This is primarily used for debugging.
    def plot_voxel_grid(self):
        # print("--------- plot_voxel_grid()")
        #  Should we actually parse/use coords in initial.xml, e.g.:
        #      <x_coordinates delimiter=" ">-490.000000 -470.000000
        # xoffset = self.xdel / 2.0
        # yoffset = self.ydel / 2.0
        # xmax = self.xmax - xoffset
        # xmin = self.xmin + xoffset
        # ymax = self.ymax - yoffset
        # ymin = self.ymin + yoffset

        xs = np.arange(self.xmin,self.xmax+1,self.xdel)  # DON'T try to use np.linspace!
        # print("xmin,max,del=",self.xmin,self.xmax,self.xdel)
        # print("xs= ",xs)
        ys = np.arange(self.ymin,self.ymax+1,self.ydel)
        # print("ys= ",ys)
        hlines = np.column_stack(np.broadcast_arrays(xs[0], ys, xs[-1], ys))
        vlines = np.column_stack(np.broadcast_arrays(xs, ys[0], xs, ys[-1]))
        grid_lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
        line_collection = LineCollection(grid_lines, color="gray", linewidths=0.5)
        self.ax0.add_collection(line_collection)

    #------------------------------------------------------------
    def plot_mechanics_grid(self):
        xs = np.arange(self.xmin,self.xmax+1,self.mech_voxel_size)  # DON'T try to use np.linspace!
        ys = np.arange(self.ymin,self.ymax+1,self.mech_voxel_size)
        # print(f'plot_mechanics_grid:  xs={xs} ,ys={ys}')
        hlines = np.column_stack(np.broadcast_arrays(xs[0], ys, xs[-1], ys))
        vlines = np.column_stack(np.broadcast_arrays(xs, ys[0], xs, ys[-1]))
        grid_lines = np.concatenate([hlines, vlines]).reshape(-1, 2, 2)
        line_collection = LineCollection(grid_lines, color="red", linewidths=0.7)
        # ax = plt.gca()
        # ax.add_collection(line_collection)
        self.ax0.add_collection(line_collection)
        # ax.set_xlim(xs[0], xs[-1])
        # ax.set_ylim(ys[0], ys[-1])

    #------------------------------------------------------------
    # def plot_svg(self, frame, rdel=''):
    def plot_svg(self, frame):
        # global current_idx, axes_max
        # global current_frame

        # return

        # if self.show_voxel_grid:
        #     self.plot_voxel_grid()
        # if self.show_mechanics_grid:
        #     self.plot_mechanics_grid()

        # if self.show_vectors:
        #     self.plot_vecs()

        # current_frame = frame
        # self.current_frame = frame
        fname = "snapshot%08d.svg" % frame
        full_fname = os.path.join(self.output_dir, fname)
        # print("-- plot_svg(): full_fname= ",full_fname)
        # try:
        #     print("   ==>>>>> plot_svg(): full_fname=",full_fname)
        # except:
        #     print("plot_svg(): ERROR:  full_name invalid")   
        #     return
        # with debug_view:
            # print("plot_svg:", full_fname) 
        # print("-- plot_svg:", full_fname) 
        if not os.path.isfile(full_fname):
            # print("Once output files are generated, click the slider.")   
            print("vis_tab.py: plot_svg(): Warning: full_fname not found: ",full_fname)
            return

        # self.ax0.cla()
        self.title_str = ""

# https://stackoverflow.com/questions/5263034/remove-colorbar-from-figure-in-matplotlib
# def foo(self):
#    self.subplot.clear()
#    hb = self.subplot.hexbin(...)
#    if self.cb:
#       self.figure.delaxes(self.figure.axes[1])
#       self.figure.subplots_adjust(right=0.90)  #default right padding
#    self.cb = self.figure.colorbar(hb)

        # if self.cbar:
            # self.cbar.remove()

        # bgcolor = self.bgcolor;  # 1.0 for white 
        # bgcolor = [0,0,0,1]  # dark mode

        xlist = deque()
        ylist = deque()
        rlist = deque()
        rgba_list = deque()

        #  print('\n---- ' + fname + ':')
#        tree = ET.parse(fname)
        try:
            tree = ET.parse(full_fname)
        except:
            print("------ plot_svg(): error trying to parse ",full_fname)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msg = "plot_svg(): error parsing "+full_fname+". You may have a partially written .svg file due to a canceled simulation."
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            return
        root = tree.getroot()
        #  print('--- root.tag ---')
        #  print(root.tag)
        #  print('--- root.attrib ---')
        #  print(root.attrib)
        #  print('--- child.tag, child.attrib ---')
        numChildren = 0
        for child in root:
            #    print(child.tag, child.attrib)
            #    print("keys=",child.attrib.keys())
            # if self.use_defaults and ('width' in child.attrib.keys()):
            #     self.axes_max = float(child.attrib['width'])
                # print("debug> found width --> axes_max =", axes_max)
            if child.text and "Current time" in child.text:
                svals = child.text.split()
                # remove the ".00" on minutes
                self.title_str += svals[2] + " days, " + svals[4] + " hrs, " + svals[7][:-3] + " mins"

                # self.cell_time_mins = int(svals[2])*1440 + int(svals[4])*60 + int(svals[7][:-3])
                # self.title_str += "   cells: " + str(self.cell_time_mins) + "m"   # rwh

            # print("width ",child.attrib['width'])
            # print('attrib=',child.attrib)
            # if (child.attrib['id'] == 'tissue'):
            if ('id' in child.attrib.keys()):
                # print('-------- found tissue!!')
                tissue_parent = child
                break

        # print('------ search tissue')
        cells_parent = None

        for child in tissue_parent:
            # print('attrib=',child.attrib)
            if (child.attrib['id'] == 'cells'):
                # print('-------- found cells, setting cells_parent')
                cells_parent = child
                break
            numChildren += 1

        num_cells = 0
        if self.celltype_filter:
            # if the list is not empty, filter the cells
            filtered_names = [self.cell_dict[str(k)] for k in self.celltype_filter]
            filter_out = lambda x: x.attrib['type'] not in filtered_names
        else:
            filter_out = lambda x: False # don't filter anything out

        for child in cells_parent:
            if filter_out(child):
                continue
            # print(child.tag, child.attrib)
            # print(f'------ attrib={child.attrib}\n')
            for circle in child:  # two circles in each child: outer + nucleus
                #  circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
                #      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
                try:
                    xval = float(circle.attrib['cx'])
                except:
                    continue

                # map SVG coords into comp domain
                # xval = (xval-self.svg_xmin)/self.svg_xrange * self.x_range + self.xmin
                xval = xval/self.x_range * self.x_range + self.xmin

                s = circle.attrib['fill']
                # print("s=",s)
                # print("type(s)=",type(s))
                if( s[0:4] == "rgba" ):
                    # background = bgcolor[0] * 255.0; # coudl also be 255.0 for white
                    rgba_float =list(map(float,s[5:-1].split(",")))
                    r = rgba_float[0]
                    g = rgba_float[1]
                    b = rgba_float[2]                    
                    alpha = rgba_float[3]
                    alpha *= 2.0; # cell_alpha_toggle
                    if( alpha > 1.0 ):
                    # if( alpha > 1.0 or self.cell_alpha_toggle.value == False ):
                        alpha = 1.0
                    # if( self.cell_alpha_toggle.value == False ):
                    #     alpha = 1.0;  

#                        if( self.substrates_toggle.value and 1 == 2 ):
#                            r = background * (1-alpha) + alpha*rgba_float[0];
#                            g = background * (1-alpha) + alpha*rgba_float[1];
#                            b = background * (1-alpha) + alpha*rgba_float[2];
                    rgba = [1,1,1,alpha]
                    rgba[0:3] = [ np.round(r), np.round(g), np.round(b) ]
                    rgba[0:3] = [x / 255. for x in rgba[0:3] ]  
                    # rgba = [rgba_float[0]/255.0, rgba_float[1]/255.0, rgba_float[2]/255.0,alpha];
                    # rgba[0:3] = rgb; 
                    # rgb = list(map(int, s[5:-1].split(",")))
                elif (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
                    rgba = [1,1,1,1.0]
                    rgba[0:3] = list(map(int, s[4:-1].split(",")))  
                    rgba[0:3] = [x / 255. for x in rgba[0:3] ]
                else:     # otherwise, must be a color name
                    rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
                    rgba = [1,1,1,1.0]
                    rgba[0:3] = [x for x in rgb_tuple]

                # test for bogus x,y locations (rwh TODO: use max of domain?)
                too_large_val = 10000.
                if (np.fabs(xval) > too_large_val):
                    print("bogus xval=", xval)
                    break
                yval = float(circle.attrib['cy'])
                # yval = (yval - self.svg_xmin)/self.svg_xrange * self.y_range + self.ymin
                yval = yval/self.y_range * self.y_range + self.ymin
                if (np.fabs(yval) > too_large_val):
                    print("bogus yval=", yval)
                    break

                rval = float(circle.attrib['r'])
                # if (rgb[0] > rgb[1]):
                #     print(num_cells,rgb, rval)
                xlist.append(xval)
                ylist.append(yval)
                rlist.append(rval)
                rgba_list.append(rgba)

                # For .svg files with cells that *have* a nucleus, there will be a 2nd
                if (not self.show_nucleus):
                #if (not self.show_nucleus):
                    break

            num_cells += 1

            # if num_cells > 3:   # for debugging
            #   print(fname,':  num_cells= ',num_cells," --- debug exit.")
            #   sys.exit(1)
            #   break

            # print(fname,':  num_cells= ',num_cells)

        xvals = np.array(xlist)
        yvals = np.array(ylist)
        rvals = np.array(rlist)
        rgbas = np.array(rgba_list)
        # print("xvals[0:5]=",xvals[0:5])
        # print("rvals[0:5]=",rvals[0:5])
        # print("rvals.min, max=",rvals.min(),rvals.max())

        self.title_str += " (" + str(num_cells) + " agents)"
        self.ax0.set_title(self.title_str, fontsize=self.title_fontsize)

        self.ax0.set_xlim(self.plot_xmin, self.plot_xmax)
        self.ax0.set_ylim(self.plot_ymin, self.plot_ymax)

        self.ax0.tick_params(labelsize=self.fontsize)

        self.ax0.set_facecolor(self.bgcolor)

        if (self.cell_fill):
            if (self.cell_edge):
                try:
                    self.circles(xvals,yvals, s=rvals, color=rgbas,  edgecolor='black', linewidth=self.cell_line_width)
                except (ValueError):
                    pass
            else:
                self.circles(xvals,yvals, s=rvals, color=rgbas )
        else:  # transparent cells, but with (thicker) edges
            self.circles(xvals,yvals, s=rvals, color=(1,1,1,0),  edgecolor=rgbas, linewidth=self.cell_line_width2) 


        if self.view_aspect_square:
            self.ax0.set_aspect('equal')
        else:
            self.ax0.set_aspect('auto')
    
    #-----------------------------------------------------
    # def cell_scalar_cbar_combobox_changed_cb(self,idx):
    #     # print("\n>vis_tab-------->> cell_scalar_cbar_combobox_changed_cb(): cbar_name= ", cbar_name)
    #     self.update_plots()

    #-----------------------------------------------------
    def plot_cell_physiboss(self, frame):
        
        xml_file_root = "output%08d.xml" % frame
        xml_file = os.path.join(self.output_dir, xml_file_root)
        
        if not Path(xml_file).is_file():
            print("vis_tab.py: plot_cell_physiboss(): error file not found ",xml_file)
            return

        mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
        total_min = mcds.get_time()
        
        try:
            cell_types = mcds.get_cell_df()["cell_type"]
        except:
            print("vis_tab.py: plot_cell_physiboss(): error performing mcds.get_cell_df()['cell_type']")
            return
        
        physiboss_state_file = os.path.join(self.output_dir, "output%08d_boolean_intracellular.csv" % frame)
        
        if not Path(physiboss_state_file).is_file():
            
            physiboss_state_file = os.path.join(self.output_dir, "states_%08d.csv" % frame)
            
            if not Path(physiboss_state_file).is_file():
                print("vis_tab.py: plot_cell_physiboss(): error file not found ",physiboss_state_file)
                return
        
        cell_scalar = {id: 9 for id in mcds.get_cell_df().index}
        
        name_cellline = list(self.physiboss_node_dict.keys())[self.physiboss_selected_cell_line]
        id_cellline = list(self.celldef_tab.param_d.keys()).index(name_cellline)
        
        with open(physiboss_state_file, newline='') as csvfile:
            states_reader = csv.reader(csvfile, delimiter=',')
                
            for row in states_reader:
                if row[0] != 'ID':
                    ID = int(row[0])
                    if cell_types[ID] == id_cellline:
                        nodes = row[1].split(" -- ")             

                        if self.physiboss_selected_node in nodes:
                            cell_scalar.update({ID: 2})      
                        else:
                            cell_scalar.update({ID: 0})
                    else:
                        cell_scalar.update({ID: 9})
                        
        cell_scalar = pandas.Series(cell_scalar)
            
        # To plot green/red/grey cells, we use a qualitative cell map called Set1
        cbar_name = "Set1"
        vmin = 0
        vmax = 9
        
        num_cells = len(cell_scalar)
        cell_vol = mcds.get_cell_df()['total_volume']
        
        four_thirds_pi =  4.188790204786391
        cell_radii = np.divide(cell_vol, four_thirds_pi)
        cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

        xvals = mcds.get_cell_df()['position_x']
        yvals = mcds.get_cell_df()['position_y']

        mins = total_min
        hrs = int(mins/60)
        days = int(hrs/24)
        self.title_str = '%d days, %d hrs, %d mins' % (days, hrs-days*24, mins-hrs*60)
        self.title_str += " (" + str(num_cells) + " agents)"

        if (self.cell_edge):
            try:
                cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=self.cell_line_width, cmap=cbar_name, vmin=vmin, vmax=vmax)
            except (ValueError):
                print("\n------ ERROR: Exception from circles with edges\n")
                pass
        else:
            cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax)

        if self.graph_display_type != 'NONE':
            for c1,c2 in self.attachments:
                self.ax0.plot([xvals[c1], xvals[c2]], [yvals[c1], yvals[c2]], 'k-', lw=0.5)
    
        if self.cax2:
            try:
                self.cax2.remove()
                self.cax2 = None
            except:
                pass
   
        self.ax0.set_title(self.title_str, fontsize=self.title_fontsize)
        self.ax0.set_xlim(self.plot_xmin, self.plot_xmax)
        self.ax0.set_ylim(self.plot_ymin, self.plot_ymax)

        if self.view_aspect_square:
            self.ax0.set_aspect('equal')
        else:
            self.ax0.set_aspect('auto')
        
        names_observed = ["Active", "Inactive", "Other cell type"]
        boolean_colors = ["green", "red", "grey"]
        
        # Creating empty plots to add the legend
        lp = lambda i: plt.plot([],color=boolean_colors[i], ms=np.sqrt(81), mec="none",
                                label="Feature {:g}".format(i), ls="", marker="o")[0]
        handles = [lp(i) for i in range(3)]
        try: # cautionary for out of date mpl versions, e.g., nanoHUB
            self.ax0.legend(handles=handles,labels=names_observed, loc='upper center', bbox_to_anchor=(0.5, -0.15),ncols=4)
        except:
            pass
    
    def plot_cell_scalar(self, frame):
        if self.disable_cell_scalar_cb:
            return
            
        # if self.show_voxel_grid:
        #     self.plot_voxel_grid()
        # if self.show_mechanics_grid:
        #     self.plot_mechanics_grid()


        xml_file_root = "output%08d.xml" % frame
        xml_file = os.path.join(self.output_dir, xml_file_root)
        cell_scalar_humanreadable_name = self.cell_scalar_combobox.currentText()
        if cell_scalar_humanreadable_name in self.cell_scalar_human2mcds_dict.keys():
            cell_scalar_mcds_name = self.cell_scalar_human2mcds_dict[cell_scalar_humanreadable_name]
        else:
            cell_scalar_mcds_name = cell_scalar_humanreadable_name
        cbar_name = self.cell_scalar_cbar_combobox.currentText()
        if not Path(xml_file).is_file():
            print("ERROR: file not found",xml_file)
            return

        mcds = pyMCDS(xml_file_root, self.output_dir, microenv=False, graph=False, verbose=False)
        df_cells = self.get_mcds_cells_df(mcds)
        total_min = mcds.get_time()  # warning: can return float that's epsilon from integer value

        try:
            cell_scalar = df_cells[cell_scalar_mcds_name]
        except:
            print("vis_tab.py: plot_cell_scalar(): error performing df_cells[cell_scalar_mcds_name]")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msg = "plot_cell_scalar(): error from df_cells[" + cell_scalar_mcds_name + "]. You may be trying to use out-of-date scalars. Please reset the 'full list' or 'partial'."
            msgBox.setText(msg)
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
            # kill any animation ("Play" button) happening
            self.animating_flag = False
            self.play_button.setText("Play")
            self.timer.stop()

            # self.cells_svg_rb.setChecked(True)
            # self.plot_cells_svg = True
            # self.disable_cell_scalar_widgets()
            return
                
        if self.fix_cells_cmap_flag:
            vmin = self.cells_cmin_value
            vmax = self.cells_cmax_value
        else:
            vmin = cell_scalar.min()
            vmax = cell_scalar.max()
            
        num_cells = len(cell_scalar)
        # print("  len(cell_scalar) = ",len(cell_scalar))
        # fix_cmap = 0
        # print(f'   cell_scalar.min(), max() = {vmin}, {vmax}')
        cell_vol = df_cells['total_volume']
        # print(f'   cell_vol.min(), max() = {cell_vol.min()}, {cell_vol.max()}')

        four_thirds_pi =  4.188790204786391
        cell_radii = np.divide(cell_vol, four_thirds_pi)
        cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

        xvals = df_cells['position_x']
        yvals = df_cells['position_y']

        # self.title_str += "   cells: " + svals[2] + "d, " + svals[4] + "h, " + svals[7][:-3] + "m"
        # self.title_str = "(" + str(frame) + ") Current time: " + str(total_min) + "m"
        
        if cell_scalar_mcds_name in self.discrete_cell_scalars: 

            self.discrete_variable_observed = self.discrete_variable_observed.union(set([int(i) for i in np.unique(cell_scalar)]))

            if cell_scalar_mcds_name == "current_phase":   # and if "Fixed" range is checked
                self.discrete_variable = list(self.cycle_phases.keys())
                names_observed = [self.cycle_phases[i] for i in sorted(list(self.discrete_variable_observed)) if i in self.cycle_phases.keys()]

            elif cell_scalar_mcds_name == "cell_type":
                # I'm not sure I should be calling this every time. But I'm also not sure about the life cycle of celltype_name
                self.get_cell_types_from_config()
                self.discrete_variable = list(range(len(self.celltype_name)))
                names_observed = [self.celltype_name[i] for i in sorted(list(self.discrete_variable_observed)) if i < len(self.celltype_name)]
                
            elif cell_scalar_mcds_name == "cycle_model":
                self.discrete_variable = list(self.cycle_models.keys())
                names_observed = [self.cycle_models[i] for i in sorted(list(self.discrete_variable_observed)) if i in self.cycle_models.keys()]

            elif cell_scalar_mcds_name == "current_death_model":
                self.discrete_variable = [0,1]
                names_observed = ["phase #%d" % i for i in sorted(list(self.discrete_variable_observed)) if i in [0,1]]
            
            elif cell_scalar_mcds_name == "is_motile":
                self.discrete_variable = [0,1]
                names_observed = ["motile" if i == 1 else "stationnary" for i in sorted(list(self.discrete_variable_observed)) if i in [0,1]]
                
            elif cell_scalar_mcds_name == "dead":
                self.discrete_variable = [0,1]
                names_observed = ["dead" if i == 1 else "alive" for i in sorted(list(self.discrete_variable_observed)) if i in [0,1]]
            else:
                self.discrete_variable = [int(i) for i in list(set(cell_scalar))] # It's a set of possible value of the variable
                names_observed = [str(int(i)) for i in sorted(list(self.discrete_variable_observed))] 

        # if( discrete_variable ): # Generic way: if variable is discrete
            self.cell_scalar_cbar_combobox.setEnabled(False)
            from_list = matplotlib.colors.LinearSegmentedColormap.from_list
            self.discrete_variable.sort()
            if (len(self.discrete_variable) == 1): 
                cbar_name = from_list(None, cmaps.gray_gray[0:2], len(self.discrete_variable))  # annoying hack
            else: 
                try:
                    cbar_name = from_list(None, cmaps.paint_clist[0:len(self.discrete_variable)], len(self.discrete_variable))
                except:
                    return

            # usual categorical colormap on matplotlib has at max 20 colors (using colorcet the colormap glasbey_bw has n colors )
            # cbar_name = from_list(None, cc.glasbey_bw, len(self.discrete_variable))
            vmin = None
            vmax = None
            # Change the values between 0 and number of possible values
            for i, value in enumerate(self.discrete_variable):
                cell_scalar = cell_scalar.replace(value,i)
                # print("cell_scalar=",cell_scalar)
        else: 
            self.cell_scalar_cbar_combobox.setEnabled(True)
            self.discrete_variable = None
            self.discrete_variable_observed = set()
            
        mins = round(total_min)  # hack, assume we want integer mins
        hrs = int(mins/60)
        days = int(hrs/24)
        # print(f"mins={mins}, hrs={hrs}, days={days}")
        self.title_str = '%d days, %d hrs, %d mins' % (days, hrs-days*24, mins-hrs*60)
        # self.title_str = '%f mins' % (total_min)  # rwh: custom
        self.title_str += " (" + str(num_cells) + " agents)"

        axes_min = mcds.get_mesh()[0][0][0][0]
        axes_max = mcds.get_mesh()[0][0][-1][0]

        if (self.cell_fill):
            if (self.cell_edge):
                try:
                    # print("plot circles with vmin,vmax=",vmin,vmax)  # None,None
                    # print("plot circles with cbar_name=",cbar_name)  # <matplotlib.colors.LinearSegmentedColormap object at 0x1690d5330>
                    cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=self.cell_line_width, cmap=cbar_name, vmin=vmin, vmax=vmax)
                    # cell_plot = self.circles(xvals,yvals, s=cell_radii, edgecolor=cell_scalar, linewidth=0.5, cmap=cbar_name, vmin=vmin, vmax=vmax)
                except (ValueError):
                    print("\n------ ERROR: Exception from circles with edges\n")
                    pass
            else:
                # cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name)
                cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax)

        else:  # semi-trransparent cell, but with (thicker) edge  (TODO: how to make totally transparent?)
            if (self.cell_edge):
                cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=self.cell_line_width2, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=self.cell_alpha)
            else:
                cell_plot = self.circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=self.cell_alpha)


        # print("------- plot_cell_scalar() -------------")
        num_axes =  len(self.figure.axes)
        # print("# axes = ",num_axes)
        # if num_axes > 1: 
        # if self.axis_id_cellscalar:
    
        if( self.discrete_variable ): # Generic way: if variable is discrete
            # Then we don't need the cax2
            if self.cax2 is not None:
                try:
                    self.cax2.remove()
                    self.cax2 = None
                except:
                    pass
            # Coloring the cells as it used to be
            cell_plot.set_clim(vmin=-0.5,vmax=len(self.discrete_variable)-0.5) 
            
            # Creating empty plots to add the legend
            lp = lambda i: plt.plot([],color=cmaps.paint_clist[i], ms=np.sqrt(81), mec="none",
                                    label="Feature {:g}".format(i), ls="", marker="o")[0]
            handles = [lp(self.discrete_variable.index(i)) for i in sorted(list(self.discrete_variable_observed)) if i in self.discrete_variable]
            try: # cautionary for out of date mpl versions, e.g., nanoHUB
                self.ax0.legend(handles=handles,title=cell_scalar_humanreadable_name, labels=names_observed, loc='upper center', bbox_to_anchor=(0.5, -0.15),ncols=4)
            except:
                pass

        else:   # Note: vis_tab_ecm.py seems to avoid any memory leak and with simpler code
            # If it's not there, we create it
            if self.cax2 is None:
                self.cax2 = self.figure.add_subplot(self.gs[1,0])
                # ax2_divider = make_axes_locatable(self.ax0)
                # self.cax2 = ax2_divider.append_axes("bottom", size="4%", pad="8%")
            if self.cbar2 is None:
                self.cbar2 = self.figure.colorbar(cell_plot, ticks=None, cax=self.cax2, orientation="horizontal")
                self.cbar2.ax.tick_params(labelsize=self.fontsize)
            elif self.cell_scalar_updated:
                self.cbar2 = self.figure.colorbar(cell_plot, ticks=None, cax=self.cax2, orientation="horizontal")
                self.cell_scalar_updated = False
            else:
                self.cbar2.update_normal(cell_plot)  # partial fix for memory leak

            self.cbar2.ax.set_xlabel(cell_scalar_humanreadable_name, fontsize=self.cbar_label_fontsize)
   
        self.ax0.set_title(self.title_str, fontsize=self.title_fontsize)
        self.ax0.set_xlim(self.plot_xmin, self.plot_xmax)
        self.ax0.set_ylim(self.plot_ymin, self.plot_ymax)

        if self.view_aspect_square:
            self.ax0.set_aspect('equal')
        else:
            self.ax0.set_aspect('auto')


    #------------------------------------------------------------
    def plot_substrate(self, frame):

        # f=1/0  # force segfault
        xml_file_root = "output%08d.xml" % frame
        xml_file = os.path.join(self.output_dir, xml_file_root)
        if not Path(xml_file).is_file():
            print("ERROR: file not found",xml_file)
            return

        cbar_name = self.substrates_cbar_combobox.currentText()

        # xml_file = os.path.join(self.output_dir, xml_file_root)
        tree = ET.parse(xml_file)
        root = tree.getroot()
    #    print('time=' + root.find(".//current_time").text)
        mins = float(root.find(".//current_time").text)
        hrs = int(mins/60)
        days = int(hrs/24)
        self.title_str = '%d days, %d hrs, %d mins' % (days,hrs-days*24, mins-hrs*60)
        # print(self.title_str)

        fname = "output%08d_microenvironment0.mat" % frame
        full_fname = os.path.join(self.output_dir, fname)
        # print("\n    ==>>>>> plot_substrate(): full_fname=",full_fname)
        if not Path(full_fname).is_file():
            print("ERROR: file not found",full_fname)
            return

        info_dict = {}
        scipy.io.loadmat(full_fname, info_dict)
        M = info_dict['multiscale_microenvironment']
        # print('plot_substrate: self.field_index=',self.field_index)

        # debug
        # fsub = M[self.field_index,:]   # 
        # print("substrate min,max=",fsub.min(), fsub.max())

        # print("M.shape = ",M.shape)  # e.g.,  (6, 421875)  (where 421875=75*75*75)
        # numx = int(M.shape[1] ** (1./3) + 1)
        # numy = numx
        # self.numx = 50  # for template model
        # self.numy = 50
        # self.numx = 88  # for kidney model
        # self.numy = 75

        # try:
        #     print("plot_substrate(): self.numx, self.numy = ",self.numx, self.numy )
        # except:
        #     print("Error: self.numx, self.numy not defined.")
        #     return
        # nxny = numx * numy

        try:
            xgrid = M[0, :].reshape(self.numy, self.numx)
            ygrid = M[1, :].reshape(self.numy, self.numx)
        except:
            # print("error: cannot reshape ",self.numy, self.numx," for array ",M.shape)
            print("vis_tab.py: unable to reshape substrate array; return")
            return

        zvals = M[self.field_index,:].reshape(self.numy,self.numx)
        try:
            zvals = M[self.field_index,:].reshape(self.numy,self.numx)
            # print("zvals.min(), max() = ",zvals.min(),zvals.max())
        except:
            print("vis_tab.py:  zvals Exception; return")
            return

        if (self.substrate_grad):
            try:
                # print(zvals.shape, ygrid[:,0], xgrid[0,:])
                grad_x, grad_y = np.gradient(zvals, ygrid[:,0], xgrid[0,:])
                zvals = np.sqrt(grad_x**2 + grad_y**2)
                # print(zvals.min(),zvals.max())
            except:
                print("vis_tab.py: unable to compute the substrate gradient.")


        contour_ok = True
        # if (self.colormap_fixed_toggle.value):
        # self.field_index = 4

        if (self.contour_mesh):
            if (self.fix_cmap_flag):
                try:
                    substrate_plot = self.ax0.pcolormesh(xgrid,ygrid, zvals, shading=self.shading_choice, cmap=cbar_name, vmin=self.cmin_value, vmax=self.cmax_value)
                except:
                    contour_ok = False
                    print('\nWARNING: exception with fixed colormap range. Will not update plot.')
            else:    
                try:
                    # substrate_plot = self.ax0.contourf(xgrid, ygrid, zvals, self.num_contours, cmap=cbar_name)  # self.colormap_dd.value)

                    substrate_plot = self.ax0.pcolormesh(xgrid,ygrid, zvals, shading=self.shading_choice, cmap=cbar_name) #, vmin=Z.min(), vmax=Z.max())
                except:
                    contour_ok = False
                    print('\nWARNING: exception with dynamic colormap range. Will not update plot.')

        if (self.contour_lines):
            if (self.fix_cmap_flag):
                try:
                    delstep = (self.cmax_value - self.cmin_value) / 8
                    levels = np.arange(self.cmin_value + delstep, self.cmax_value, delstep)
                    substrate_plot = self.ax0.contour(xgrid,ygrid,zvals, levels=levels, cmap=cbar_name, vmin=self.cmin_value, vmax=self.cmax_value)  # contour lines
                except:
                    print("vis_tab: No contour levels were found within the data range.")
                    return
            else:    
                try:
                    substrate_plot = self.ax0.contour(xgrid,ygrid,zvals, cmap=cbar_name)  # contour lines
                except:
                    print("vis_tab: No contour levels were found within the data range.")
                    return

        # in case we want to plot a "0.0" contour line
        # if self.field_index > 4:
        #     self.ax0.contour(xgrid, ygrid, M[self.field_index, :].reshape(self.numy,self.numx), [0.0], linewidths=0.5)

        # Do this funky stuff to prevent the colorbar from shrinking in height with each redraw.
        # Except it doesn't seem to work when we use fixed ranges on the colorbar?!
        # print("------- plot_substrate() -------------")
        num_axes =  len(self.figure.axes)
        # print("# axes = ",num_axes)
        if self.cax1:
            self.cax1.remove()  # replace/update the colorbar
            # print("# axes(after substrate remove) = ",len(self.figure.axes))
            # print(" self.figure.axes= ",self.figure.axes)
            #ppp
            # ax1_divider = make_axes_locatable(self.ax0)
            # self.cax1 = ax1_divider.append_axes("right", size="4%", pad="2%")
            self.cax1 = self.figure.add_subplot(self.gs[0,1])
            try:
                self.cbar1 = self.figure.colorbar(substrate_plot, cax=self.cax1)
            except:
                print("vis_tab: No contour levels were found within the data range.")
            # print("\n# axes(redraw substrate) = ",len(self.figure.axes))
            # print(" self.figure.axes= ",self.figure.axes)
            self.cbar1.ax.tick_params(labelsize=self.fontsize)
        else:
            # ax1_divider = make_axes_locatable(self.ax0)
            # self.cax1 = ax1_divider.append_axes("right", size="4%", pad="2%")
            self.cax1 = self.figure.add_subplot(self.gs[0,1])
            try:
                self.cbar1 = self.figure.colorbar(substrate_plot, cax=self.cax1)
            except:
                print("vis_tab: No contour levels were found within the data range.")
                return
            self.cbar1.ax.tick_params(labelsize=self.fontsize)
            # print("(init substrate) self.figure.axes= ",self.figure.axes)

        self.cbar1.set_label(self.substrate_name)
        if (self.substrate_grad):
            self.cbar1.set_label(self.substrate_name + " (gradient norm)", fontsize=self.cbar_label_fontsize)
        else:
            self.cbar1.set_label(self.substrate_name, fontsize=self.cbar_label_fontsize)

        self.ax0.set_title(self.title_str, fontsize=self.title_fontsize)
        self.ax0.set_xlim(self.plot_xmin, self.plot_xmax)
        self.ax0.set_ylim(self.plot_ymin, self.plot_ymax)

        if self.view_aspect_square:
            self.ax0.set_aspect('equal')
        else:
            self.ax0.set_aspect('auto')
