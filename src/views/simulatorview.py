#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from kivy.uix.widget import Widget
from materialwidget import MaterialWidget
from graphview import GraphView
from circuitview import CircuitView
from materialbutton import MaterialButton
from kivy.properties import ObjectProperty
from playbackcontrolview import PlaybackControlView

class SimulatorView(Widget):
    """
    The root widget containing all the views.
    """
    model = ObjectProperty(None)
    graphView = ObjectProperty(None)
    playbackControlView = ObjectProperty(None)
    circuitView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SimulatorView, self).__init__(**kwargs)


    def on_model(self, *args, **kwargs):
        self.graphView.model = self.model
        self.circuitView.model = self.model
        self.playbackControlView.model = self.model
    

    def update(self, dt):
        self.graphView.update(dt)
        self.playbackControlView.update(dt)
        self.circuitView.setGraphBounds(self.graphView.getBounds())