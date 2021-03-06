#!/usr/bin/env python
from python_qt_binding.QtCore import Slot, Qt, QTimer, qWarning, Signal
from python_qt_binding.QtGui import QWidget, QVBoxLayout, QSizePolicy, QColor
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import operator
import numpy as np
import copy, threading
import rospy
from trajectory_msgs.msg import JointTrajectory

class PlotCanvas(FigureCanvas):
    def __init__(self):
        super(PlotCanvas, self).__init__(Figure())
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True, color='gray')
        self.figure.tight_layout()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)
        # create widgets
        self.canvas = PlotCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self.canvas)
        self.toolbar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        vbox = QVBoxLayout()
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)
        self.setLayout(vbox)

    def draw_curves (self, curve_names, data):
        self.canvas.axes.clear()
        self.canvas.axes.grid(True, color='gray')
        for name in curve_names:
            xdata, ydata = data[name]
            self.canvas.axes.plot(xdata, ydata, 'o-', label=name)[0]
        self.update_legend()
        self.canvas.draw()

    def update_legend(self):
        handles, labels = self.canvas.axes.get_legend_handles_labels()
        self.canvas.axes.legend(handles, labels, loc='upper left')
