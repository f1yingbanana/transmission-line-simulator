#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-21-2017
#

import matplotlib.pyplot as plt
import numpy as np
from materialwidget import MaterialWidget
from kivy.properties import *
from util.constants import *

class OscilloscopeGraphView(MaterialWidget):
    """
    This manages the display of a specific oscilloscope, with functions to zoom,
    pan, export, and value display.
    """
    container = ObjectProperty(None)


    def __init__(self, oscilloscope, **kwargs):
        super(OscilloscopeGraphView, self).__init__(**kwargs)

        self.oscilloscope = oscilloscope

        self._line = None
        self._fig, self._ax = plt.subplots()
        self._fig.set_tight_layout({"pad": 3})
        self._ax.grid(True)
        self._ax.set_ylabel('voltage (V)', fontsize = 16)
        self._ax.set_xlabel('time (ns)', fontsize = 16)

        # How big is the graph, in ns.
        self.window = 20

        for item in self._ax.get_yticklabels() + self._ax.get_xticklabels():
            item.set_fontsize(16)
        
        for i in self._ax.spines.itervalues():
            i.set_linewidth(4)
        
        self.container.add_widget(self._fig.canvas)


    def update(self, dt):
        if not self.oscilloscope.isRecording():
            return

        if self._line == None:
            self._line = self._ax.plot(self.oscilloscope.graph[0], self.oscilloscope.graph[1], \
                linewidth = 4, color = PRIMARY)[0]
        else:
            self._line.set_xdata(self.oscilloscope.graph[0])
            self._line.set_ydata(self.oscilloscope.graph[1])
            c = self.oscilloscope.graph[0][-1]
            self._ax.set_xlim([c - self.window, c])
            v = max(max(self.oscilloscope.graph[1]), abs(min(self.oscilloscope.graph[1])))
            v = max(v, 1)
            self._ax.set_ylim([-1.2 * v, 1.2 * v])

        self._fig.canvas.draw()

