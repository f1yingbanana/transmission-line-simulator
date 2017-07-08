#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from kivy.uix.widget import Widget
from materialwidget import MaterialWidget
from graphview import GraphView
from materialbutton import MaterialButton
from kivy.properties import ObjectProperty

class SimulatorView(Widget):
    """
    The root widget containing all the views.
    """
    
    graphView = ObjectProperty(None)
    
    def update(self, dt):
        self.graphView.update(dt)
    