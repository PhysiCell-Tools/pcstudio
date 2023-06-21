import sys
from time import sleep
import traceback

from PyQt5.QtCore import *
# from PyQt5.QtWidgets import (
#     QApplication,
#     QLabel,
#     QMainWindow,
#     QPushButton,
#     QVBoxLayout,
#     QWidget,
# )


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int, str)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Tasks(QObject):
    result: object

    def __init__(self):
        super(Tasks, self).__init__()

        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(1)
        self.signals = WorkerSignals()

    def process_result(self, result):
        self.signals.result.emit(result)

    def start(self, process_fn, *args):
        worker = Worker(process_fn, *args)
        worker.signals.result.connect(self.process_result)
        self.pool.start(worker)
        # self.pool.waitForDone()


class HubFiles():
     def __init__(self, parent=None):
         self.thread_pool = QThreadPool()

    def reportProgress(self, n, info):
        self.stepLabel.setText(f"Long-Running Step: {n}")

    def runLongTask(self, progress_callback=None):
        """Long-running task in 5 steps."""
        for i in range(10):
            sleep(1)
            count = i + self.test_int
            progress_callback.emit(count, str(count))

    def start_long_task1(self):
        self.longRunningBtn.setEnabled(False)
        worker = Worker(self.runLongTask)
        worker.signals.progress.connect(self.reportProgress)
        worker.signals.finished.connect(lambda: self.longRunningBtn.setEnabled(True))
        # pool = QThreadPool.globalInstance()
        self.thread_pool.start(worker)

    def reportProgress1(self, n, info):
        self.stepLabel1.setText(f"Long-Running Step: {n}")

# class Window(QMainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.clicksCount = 0
#         self.setupUi()

#     def setupUi(self):
#         self.setWindowTitle("Freezing GUI")
#         self.resize(300, 150)
#         self.centralWidget = QWidget()
#         self.setCentralWidget(self.centralWidget)
#         # Create and connect widgets
#         self.clicksLabel = QLabel("Counting: 0 clicks", self)
#         self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         self.stepLabel = QLabel("Long-Running Step: 0")
#         self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         self.countBtn = QPushButton("Click me!", self)
#         self.countBtn.clicked.connect(self.countClicks)
#         self.longRunningBtn = QPushButton("Long-Running Task 1", self)
#         self.longRunningBtn.clicked.connect(self.start_long_task1)

#         self.stepLabel1 = QLabel("Long-Running Step: 0")
#         self.stepLabel1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#         self.longRunningBtn1 = QPushButton("Long-Running Task 2", self)
#         self.longRunningBtn1.clicked.connect(self.start_long_task2)
#         # Set the layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.clicksLabel)
#         layout.addWidget(self.countBtn)
#         layout.addStretch()
#         layout.addWidget(self.stepLabel)
#         layout.addWidget(self.longRunningBtn)
#         layout.addStretch()
#         layout.addWidget(self.stepLabel1)
#         layout.addWidget(self.longRunningBtn1)
#         self.centralWidget.setLayout(layout)
#         self.thread_pool = QThreadPool()
#         self.test_int = 1

#     def countClicks(self):
#         self.clicksCount += 1
#         self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

#     def reportProgress(self, n, info):
#         self.stepLabel.setText(f"Long-Running Step: {n}")

#     def runLongTask(self, progress_callback=None):
#         """Long-running task in 5 steps."""
#         for i in range(10):
#             sleep(1)
#             count = i + self.test_int
#             progress_callback.emit(count, str(count))

#     def start_long_task1(self):
#         self.longRunningBtn.setEnabled(False)
#         worker = Worker(self.runLongTask)
#         worker.signals.progress.connect(self.reportProgress)
#         worker.signals.finished.connect(lambda: self.longRunningBtn.setEnabled(True))
#         # pool = QThreadPool.globalInstance()
#         self.thread_pool.start(worker)

#     def reportProgress1(self, n, info):
#         self.stepLabel1.setText(f"Long-Running Step: {n}")

#     def start_long_task2(self):
#         self.longRunningBtn1.setEnabled(False)
#         worker = Worker(self.runLongTask)
#         worker.signals.progress.connect(self.reportProgress1)
#         worker.signals.finished.connect(lambda: self.longRunningBtn1.setEnabled(True))
#         self.thread_pool.start(worker)



# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = Window()
#     win.show()
#     sys.exit(app.exec())
