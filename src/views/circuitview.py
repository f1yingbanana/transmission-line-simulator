#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-9-2017
#

from kivy.uix.widget import Widget
from materialwidget import MaterialWidget
from kivy.properties import *


class CircuitView(MaterialWidget):
    """
    This is dedicated in displaying and editing the circuit.

    model:  the simulation model.
    """

    _begin = ListProperty([0, 0])
    _end = ListProperty([0, 0])


    def __init__(self, **kwargs):
        """
        Initializes the view without drawing anything.
        """
        super(CircuitView, self).__init__(**kwargs)
        
        self.model = None


    def setGraphBounds(self, box):
        """
        This takes the graph positions and aligns itself with the graph.

        box:    a bounding box in the format of [x, y, width, height]
        """
        self._begin = box[0], self.y + self.height * 0.2
        self._end = box[0] + box[2], self.y + self.height * 0.8

        print self._begin, self._end
        print self.pos

    def update(self, dt):
        """
        Updates this instance.
        """


# Below are graphics helper classes for drawing various elements.
class Connector(Widget):
    """
    This renders a connector between two wires.
    """


class Wire(Widget):
    """
    This renders a wire.
    """


class Oscilloscope(Widget):
    """
    This renders an oscilloscope.
    """


class Load(Widget):
    """
    This renders a load.
    """


class Source(Widget):
    """
    This renders the signal source.
    """


