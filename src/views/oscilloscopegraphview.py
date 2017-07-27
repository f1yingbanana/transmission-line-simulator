#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-21-2017
#

import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import *
import numpy as np
from materialwidget import MaterialWidget
from kivy.properties import *
from util.constants import *
from util.hoverbehavior import HoverBehavior
from kivy.metrics import *
from exportdialog import ExportDialog

class OscilloscopeGraphView(MaterialWidget, HoverBehavior):
    """
    This manages the display of a specific oscilloscope, with functions to zoom,
    pan, export, and value display.
    """
    container = ObjectProperty(None)
    coordLabel = ObjectProperty(None)


    def __init__(self, oscilloscope, **kwargs):
        super(OscilloscopeGraphView, self).__init__(**kwargs)

        self.oscilloscope = oscilloscope
        self.dialogLayer = None

        self._line = None
        self._fig, self._ax = plt.subplots()
        self._fig.set_tight_layout({"pad": 3})
        self._ax.grid(True)
        self._ax.set_ylabel('voltage (V)', fontsize = 16)
        self._ax.set_xlabel('time (ns)', fontsize = 16)

        # A list of computed maximum values.
        self._maxima = []

        # This is the number of points we look before and after a given point to
        # determine whether that point is a local maximum.
        self._maximaHalfWindow = 5

        # This is the index of the last point we computed maxima for.
        self._lastCheckedIndex = 0

        # How big is the graph, in ns.
        self.window = 20

        for item in self._ax.get_yticklabels() + self._ax.get_xticklabels():
            item.set_fontsize(16)
        
        for i in self._ax.spines.itervalues():
            i.set_linewidth(4)
        
        self.container.add_widget(self._fig.canvas)


    def update(self, dt):
        # Update maxima
        self._updateMaxima()

        # Draw a cursor if mouse is close to one of the data points, and display
        # it.
        self._markCoord()

        # Update graph
        if not self.oscilloscope.isRecording():
            return

        if self._line == None:
            self._line = self._ax.plot(self.oscilloscope.graph[0], self.oscilloscope.graph[1], \
                linewidth = 4, color = hsv_to_rgb(self.oscilloscope.color))[0]
            self._line.set_marker((4, 0, 0))
            self._line.set_markevery([])
            self._line.set_markersize(dp(5))
        else:
            self._line.set_xdata(self.oscilloscope.graph[0])
            self._line.set_ydata(self.oscilloscope.graph[1])
            c = self.oscilloscope.graph[0][-1]
            self._ax.set_xlim([c - self.window, c])
            v = max(max(self.oscilloscope.graph[1]), abs(min(self.oscilloscope.graph[1])))
            v = max(v, 1)
            self._ax.set_ylim([-1.2 * v, 1.2 * v])

        self._fig.canvas.draw()


    def _updateMaxima(self):
        # Return if we already checked.
        while self._lastCheckedIndex < len(self.oscilloscope.graph[0]):
            v = self.oscilloscope.graph[1][self._lastCheckedIndex]
            self._lastCheckedIndex += 1

            # We don't have enough points...
            if self._lastCheckedIndex < self._maximaHalfWindow * 2 + 1:
                continue

            # We have enough points, and we can determine whether a point is max
            winStart = self._lastCheckedIndex - self._maximaHalfWindow * 2 - 1

            mx = max(self.oscilloscope.graph[1][winStart : self._lastCheckedIndex])
            mn = min(self.oscilloscope.graph[1][winStart : self._lastCheckedIndex])

            if mx - mn == 0:
                # It is flat. Next.
                continue

            checkedPt = self._lastCheckedIndex - self._maximaHalfWindow - 1

            if self.oscilloscope.graph[1][checkedPt] == mx:
                self._maxima.append(checkedPt)


    def _markCoord(self):
        if self._line == None:
            return

        if not self.hovered:
            self._line.set_markevery([])
            self.coordLabel.text = ''
            return

        # First, transform the mouse position to plot position
        mp = self._ax.transData.inverted().transform([self.pointerPos[0] - self.x, self.pointerPos[1] - self.y])

        # Next, determine which point to highlight. If there is a local maxima
        # nearby, detect and highlight that. Otherwise, just highlight the
        # nearest point.
        sp1 = self._ax.get_ylim()
        sp2 = self._ax.get_xlim()
        minDist = (0.01 * (sp1[0] - sp1[1]) ** 2 + 0.01 * (sp2[0] - sp2[1]) ** 2) ** 0.5
        idx = None

        for i in self._maxima:
            x = self.oscilloscope.graph[0][i]
            y = self.oscilloscope.graph[1][i]
            d = ((mp[0] - x) ** 2 + (mp[1] - y) ** 2) ** 0.5

            if d < minDist:
                minDist = d
                idx = i

        if idx == None:
            # Now we try find an ordinary point instead
            for i in range(len(self.oscilloscope.graph[0])):
                x = self.oscilloscope.graph[0][i]
                y = self.oscilloscope.graph[1][i]
                d = ((mp[0] - x) ** 2 + (mp[1] - y) ** 2) ** 0.5

                if d < minDist:
                    minDist = d
                    idx = i

        if idx != None:
            # Mark a point on the graph.
            self._line.set_markevery([idx])
            x = self.oscilloscope.graph[0][idx]
            y = self.oscilloscope.graph[1][idx]
            rawPos = self._ax.transData.transform([x, y]).tolist()
            self.coordLabel.pos = rawPos[0] + self.x, rawPos[1] + self.y
            self.coordLabel.text = '({:g}, {:g})'.format(x, y)
        else:
            self._line.set_markevery([])
            self.coordLabel.text = ''


    def reset(self):
        self._maxima = []
        self._lastCheckedIndex = 0


    def onExportButtonClick(self):
        """
        Begins the export process by bringing up a dialog.
        """
        exportDialog = ExportDialog()
        exportDialog.onConfirmClicked.append(self.exportData)
        exportDialog.show(self.dialogLayer)
        exportDialog.titleLabel.text = "Export Graph and Data"
        exportDialog.subtitleLabel.text = "Saves the graph and data captured by this oscilloscope to the 'export' folder of this applet."
        exportDialog.textField.title = "Filename"
        exportDialog.textField.text = datetime.datetime.now().strftime("SimData %Y-%m-%d %H:%M:%S")
    

    def exportData(self, path):
        """
        Exports the current data and graph to the given path.
        """
        root = ROOT_PATH

        self._fig.canvas.print_png(root + '/export/' + path + '.png')

        with open(root + '/export/' + path + '.csv', "w") as f:
            f.write('Time (ns), Amplitude(V)')
            for i in range(len(self.oscilloscope.graph[0])):
                x = str(self.oscilloscope.graph[0][i])
                y = str(self.oscilloscope.graph[1][i])
                f.write(x + ', ' + y + '\n')
