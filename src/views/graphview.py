#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-28-2017
#

from materialwidget import MaterialWidget
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from util.constants import *
from kivy.clock import Clock
from kivy.properties import *
from kivy.metrics import *

class GraphView(MaterialWidget):
    """
    This displays and constantly updates a graph with the given list of data
    using matplotlib with a kivy backend script.

    model:  the model of the simulation.
    """

    container = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        """
        Initializes the view with a flat graph.
        """
        super(GraphView, self).__init__(**kwargs)
        
        self.model = None
        self._line = None
        self._p0 = [0, 0]
        self._p1 = self.size
        
        self._fig, self._ax = plt.subplots()
        self._fig.set_tight_layout({"pad": 3})
        self._ax.grid(True)
        # self._ax.set_ylabel('Voltage (V)', fontsize = sp(16))
        self._ax.set_xlabel('Position (m)', fontsize = sp(16))
        self._ax.tick_params(axis = 'both', length = 0)
        # self._ax.set_xticklabels([])
        for item in self._ax.get_yticklabels() + self._ax.get_xticklabels():
            item.set_fontsize(sp(12))
        
        for i in self._ax.spines.itervalues():
            i.set_linewidth(dp(2))
        
        Clock.schedule_once(self._completeSetup)

    def _completeSetup(self, dt):
        self.container.add_widget(self._fig.canvas)

    def update(self, dt, active):
        """
        Redraws the graph.
        """
        if self.model != None:
            l = self.model.circuit.getLength()
            
            if self._line == None:
                self._line = self._ax.plot(self.model.graph[0], self.model.graph[1], \
                    linewidth = 5, color = PRIMARY)[0]
            else:
                self._line.set_data(self.model.graph[0], self.model.graph[1])
                self._p0 = self._ax.transAxes.transform_point([0, 0])
                self._p1 = self._ax.transAxes.transform_point([1, 1])
                v = self.model.maxAmplitude
                self._ax.set_ylim([-1.2 * v, 1.2 * v])
                self._line.set_color(PRIMARY if active else TEXT_GRAY)

            self._ax.set_xlim([0, l])


    def redrawGraph(self):
        self._fig.canvas.draw()

    
    def getBounds(self):
        """
        Returns the bounding box of the actual graph (sans labels) in our widget
        coordinates. Returns [x, y, width, height].
        """
        return [self.pos[0] + self._p0[0], self.pos[1] + self._p0[1], \
            self._p1[0] - self._p0[0], self._p1[1] - self._p0[1]]

