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
        
        x = np.linspace(0, 5, 100)
        y = np.sin(x**2)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xticks([])
        
        for item in ax.get_yticklabels():
            item.set_fontsize(24)
        
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
        
    