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

class GraphView(MaterialWidget):
    """
    This displays and constantly updates a graph with the given list of data
    using matplotlib with a kivy backend script.

    model:  the model of the simulation.
    """
    
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
        # self._ax.set_ylabel('voltage (V)', fontsize = 24)
        self._ax.tick_params(axis = 'both', length = 0)
        self._ax.set_xticklabels([])
        for item in self._ax.get_yticklabels() + self._ax.get_xticklabels():
            item.set_fontsize(24)
        
        for i in self._ax.spines.itervalues():
            i.set_linewidth(4)
        
        self.container = BoxLayout()
        self.container.add_widget(self._fig.canvas)
        self.add_widget(self.container)
        
    
    def update(self, dt):
        """
        Redraws the graph.
        """
        self.container.size = self.size
        self.container.pos = self.pos
        
        if self.model != None:
            
            if self._line == None:
                l = self.model.circuit.getLength()
                x = np.linspace(0, l, DISCRETE_STEPS + 1)
                self._line = self._ax.plot(x, self.model.overallDistribution, \
                    linewidth = 5, color = PRIMARY)[0]
                self._maxAmp = self.model.circuit.head.amplitude
                self._ax.set_ylim([-4 * self._maxAmp, 4 * self._maxAmp])
                self._ax.set_xlim([0, l])
            else:
                self._line.set_ydata(self.model.overallDistribution)
                self._p0 = self._ax.transAxes.transform_point([0, 0])
                self._p1 = self._ax.transAxes.transform_point([1, 1])
            
            self._fig.canvas.draw()

    
    def getBounds(self):
        """
        Returns the bounding box of the actual graph (sans labels) in our widget
        coordinates. Returns [x, y, width, height].
        """
        return [self.pos[0] + self._p0[0], self.pos[1] + self._p0[1], \
            self._p1[0] - self._p0[0], self._p1[1] - self._p0[1]]

