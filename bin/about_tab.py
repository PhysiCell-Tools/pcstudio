import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QFrame,QApplication,QWidget,QTabWidget,QFormLayout,QLineEdit, QHBoxLayout,QVBoxLayout,QRadioButton,QLabel,QCheckBox,QComboBox,QScrollArea, QTextEdit,QTextBrowser


class About(QWidget):
    def __init__(self, doc_absolute_path, nanohub_flag):
        super().__init__()

        self.doc_absolute_path = doc_absolute_path

        self.process = None
        
        #-------------------------------------------
        label_width = 110
        domain_value_width = 100
        value_width = 60
        label_height = 20
        units_width = 70

        self.scroll = QScrollArea()  # might contain centralWidget

        # self.text = QTextEdit()
        self.text = QTextBrowser()
        self.text.setHtml("&nbsp;")
        if nanohub_flag:
            self.text.setOpenLinks(False)
            self.text.anchorClicked.connect(self.followLink)
        else:
            self.text.setOpenExternalLinks(True)
            # self.text.setOpenLinks(True)

        fname = os.path.join(self.doc_absolute_path,"about.html")
        f = QtCore.QFile(fname)
        f.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text)
        istream = QtCore.QTextStream(f)
        self.text.setHtml(istream.readAll())
        f.close()

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(0)
        self.vbox.addStretch()


        #==================================================================
        self.text.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)

        self.scroll.setWidget(self.text) 

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.scroll)


    def followLinkFinished(self):
        self.process = None


    def followLink(self,url):
#       print(url.url())
        if not self.process:
            self.process = QtCore.QProcess()
            self.process.finished.connect(self.followLinkFinished)
            self.process.start("clientaction " + url.url())

