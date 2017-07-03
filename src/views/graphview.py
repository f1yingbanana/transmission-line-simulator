#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-28-2017
#

from cardview import CardView

import matplotlib.pyplot as plt

import numpy as np

from kivy.uix.boxlayout import BoxLayout

from util.constants import *

class GraphView(CardView):
    """
    This displays and constantly updates a graph with the given list of data
    using matplotlib with a kivy backend script.
    """
    
    def __init__(self, **kwargs):
        """
        Initializes the view with a flat graph.
        """
        super(GraphView, self).__init__(**kwargs)
        
        self.model = None
        self.line = None
        
        self.figure, self.axes = plt.subplots()
        self.axes.set_xticks([])
        
        
        for item in self.axes.get_yticklabels():
            item.set_fontsize(24)
        
        self.container = BoxLayout()
        self.container.add_widget(self.figure.canvas)
        self.add_widget(self.container)
        
    
    def update(self, dt):
        """
        Redraws the graph.
        """
        self.container.size = self.size
        self.container.pos = self.pos
        
        if self.model != None:
            
            if self.line == None:
                x = np.linspace(0, self.model.circuit.getLength(), DISCRETE_STEPS + 1)
                self.line = self.axes.plot(x, self.model.overallDistribution)[0]
                self._maxAmp = self.model.circuit.head.amplitude
                self.axes.set_ylim([-2 * self._maxAmp, 2 * self._maxAmp])
            else:
                self.line.set_ydata(self.model.overallDistribution)
            
            self.figure.canvas.draw()
        
    