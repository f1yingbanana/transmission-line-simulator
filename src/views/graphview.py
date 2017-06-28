#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-28-2017
#

from cardview import CardView

import matplotlib.pyplot as plt

import numpy as np
from kivy.garden.matplotlib.backend_kivy import FigureCanvas

from kivy.uix.boxlayout import BoxLayout

class GraphView(CardView):
    """
    This displays and constantly updates a graph with the given list of data
    using matplotlib with a kivy backend script.
    """
    
    def __init__(self, **kwargs):
        """
        Initializes the view with a flat graph.
        """
        print super(GraphView, self)
        super(GraphView, self).__init__(**kwargs)
        
        
        N = 5
        menMeans = (20, 35, 30, 35, 27)
        menStd = (2, 3, 4, 1, 2)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
        self.figure = fig
        
        self.container = BoxLayout()
        self.container.add_widget(self.figure.canvas)
        self.add_widget(self.container)
    
    def update(self, dt):
        """
        Redraws the graph.
        """
        self.container.size = self.size
        self.container.pos = self.pos
        self.figure.canvas.draw()
    