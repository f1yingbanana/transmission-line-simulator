#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-21-2017
#

from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from oscilloscopegraphview import OscilloscopeGraphView

class OscilloscopeGraphContainer(BoxLayout):
    """
    This serves as a container for all the oscilloscope graphs. Depending on
    changes in the model, this will automatically add and delete graphs.
    """

    dialogLayer = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(OscilloscopeGraphContainer, self).__init__(**kwargs)

        self.model = None


    def update(self, dt):
        if self.model == None:
            return

        # Checks whether there has been a new oscilloscope added, or reordered.
        h = self.model.circuit.headOscilloscope

        while h != None:
            found = False

            for g in self.children:
                if g.oscilloscope == h:
                    found = True
                    g.updated = True

            if not found:
                g = OscilloscopeGraphView(h)
                g.dialogLayer = self.dialogLayer
                self.add_widget(g)
                g.updated = True

            h = h.next
        
        toRemove = []

        for g in self.children:
            if g.updated:
                g.update(dt, self.model.appState)
                g.updated = False
            else:
                toRemove.append(g)

        for g in toRemove:
            self.remove_widget(g)
        

    def reset(self):
        for g in self.children:
            g.reset()
