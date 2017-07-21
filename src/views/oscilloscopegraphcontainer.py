#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-21-2017
#

from kivy.uix.boxlayout import BoxLayout
from oscilloscopegraphview import OscilloscopeGraphView

class OscilloscopeGraphContainer(BoxLayout):
    """
    This serves as a container for all the oscilloscope graphs. Depending on
    changes in the model, this will automatically add and delete graphs.
    """

    def __init__(self, **kwargs):
        super(OscilloscopeGraphContainer, self).__init__(**kwargs)

        self.model = None
        self.graphViews = []


    def update(self, dt):
        if self.model == None:
            return

        # Checks whether there has been a new oscilloscope added, or reordered.
        h = self.model.circuit.headOscilloscope

        self.clear_widgets()

        while h != None:
            found = False

            for g in self.graphViews:
                if g.oscilloscope == h:
                    found = True
                    self.add_widget(g)

            if not found:
                g = OscilloscopeGraphView(h)
                self.graphViews.append(g)
                self.add_widget(g)

            h = h.next

        for g in self.graphViews:
            g.update(dt)


    def reset(self):
        for g in self.graphViews:
            g.reset()
