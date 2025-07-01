import os
from pathlib import Path
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame,QApplication,QWidget,QTabWidget,QFormLayout,QLineEdit, QGroupBox, QHBoxLayout,QVBoxLayout,QRadioButton,QLabel,QCheckBox,QComboBox,QScrollArea,  QMainWindow,QGridLayout, QPushButton, QFileDialog, QMessageBox, QStackedWidget, QSplitter, QScrollArea

from studio_classes import DoubleValidatorWidgetBounded
# from PyQt5.QtWidgets import QCompleter, QSizePolicy
# from PyQt5.QtCore import QSortFilterProxyModel
# from PyQt5.QtSvg import QSvgWidget
# from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QIntValidator
# from PyQt5.QtCore import QRectF, Qt

class ScrollLabel(QScrollArea):
    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)

        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)


class DirDebugWindow(QWidget):
    # def __init__(self, output_dir):
    def __init__(self):   # we use vis_tab for some of the methods called
        super().__init__()

        stylesheet = """ 
            QPushButton{ border: 1px solid; border-color: rgb(145, 200, 145); border-radius: 1px;  background-color: lightgreen; color: black; width: 64px; padding-right: 8px; padding-left: 8px; padding-top: 3px; padding-bottom: 3px; } 

            """

        # self.output_dir = output_dir
        self.file_id = 0

        self.setStyleSheet(stylesheet)
        
        #-------------------------------------------
        self.scroll = QScrollArea()  # might contain centralWidget

        self.vbox = QVBoxLayout()
        glayout = QGridLayout()

        # hbox = QHBoxLayout()
        self.vbox.addLayout(glayout)

        #-------------------------------------------
        idx_row = 0
        glayout.addWidget(QLabel(f"pwd: {Path.cwd()}"), idx_row,0,1,2) # w, row, column, rowspan, colspan

        idx_row += 1
        self.show_files_button = QPushButton("dir")
        self.show_files_button.setStyleSheet("background-color: lightgreen;")
        self.show_files_button.clicked.connect(self.show_files_cb)
        glayout.addWidget(self.show_files_button, idx_row,0,1,1) # w, row, column, rowspan, colspan

        self.relative_path = QLineEdit(".")
        self.relative_path.setFixedWidth(80)
        # self.relative_path.setValidator(QIntValidator())
        # self.relative_path.textChanged.connect(self.file_id_changed)
        glayout.addWidget(self.relative_path, idx_row,1,1,1) # w, row, column, rowspan, colspan

        self.dir_files = ScrollLabel(self)
        # setting text to the label
        # dir_files = os.listdir(self.relative_path.text())
        # self.dir_files.setText(str(dir_files))
        # setting geometry
        self.dir_files.setGeometry(100, 100, 200, 80)
        
        self.vbox.addWidget(self.dir_files)

        #----------

        #----------
        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("background-color: lightgreen;")
        # self.close_button.setFixedWidth(150)
        self.close_button.clicked.connect(self.close_dir_info_cb)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.vbox.addWidget(self.close_button)
        # self.layout.setStretch(0,1000)

        self.setLayout(self.vbox)
        self.resize(200, 200)   # try to fix the size
        # self.resize(250, 220)   # try to fix the size


    #--------
    def show_info_message(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        
    def show_files_cb(self):
        dir_files = os.listdir(self.relative_path.text())
        self.dir_files.setText(str(dir_files))
        return

    #----------
    def close_dir_info_cb(self):
        self.close()

