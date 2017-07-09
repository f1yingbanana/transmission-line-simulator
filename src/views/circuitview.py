#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-9-2017
#

from kivy.uix.widget import Widget
from materialwidget import MaterialWidget
from kivy.properties import *
from models.resistor import Resistor
from models.oscilloscope import Oscilloscope


class CircuitView(MaterialWidget):
    """
    This is dedicated in displaying and editing the circuit.

    model:  the simulation model.
    """

    _begin = ListProperty([0, 0])
    _end = ListProperty([0, 0])

    model = ObjectProperty(None)


    def __init__(self, **kwargs):
        """
        Initializes the view without drawing anything.
        """
        super(CircuitView, self).__init__(**kwargs)
    

    def on_model(self, *args, **kwargs):
        self.updateCircuit()


    def setGraphBounds(self, box):
        """
        This takes the graph positions and aligns itself with the graph.

        box:    a bounding box in the format of [x, y, width, height]
        """
        self._begin = box[0], self.y + self.height * 0.2
        self._end = box[0] + box[2], self.y + self.height * 0.8
        self.updateCircuit()


    def update(self, dt):
        """
        Updates this instance.
        """


    def updateCircuit(self):
        """
        Removes all circuit elements from the diagram and add everything from
        model.
        """
        if self.model == None:
            return

        self.clear_widgets()

        # Add a source.
        source = Source()
        source.size = 80, 80
        source.center = float(self._begin[0]), float((self._begin[1] + self._end[1]) / 2)
        self.add_widget(source)

        # Add each wire and oscilloscpe with a connector inbetween.
        e = self.model.circuit.head.next
        needConnector = False
        scale = (self._end[0] - self._begin[0]) / self.model.circuit.getLength()
        c = None

        while e.next != None:
            if needConnector:
                # Create a connector in place.
                c = Connector()
                c.pos = float(self._begin[0] + e.position * scale), self._end[1]
                self.add_widget(c)
            # This element is either a wire or oscilloscope.
            if type(e) == Resistor:
                needConnector = True
                w = Wire()
                w.pos = float(self._begin[0] + e.position * scale), self._end[1]
                w.width = float(e.length * scale)
                self.add_widget(w)
            elif type(e) == Oscilloscope:
                pass
            
            # Proceed to the next element
            e = e.next

        # Add a load.
        load = Load()
        load.size = 40, 120
        load.center = float(self._end[0]), float((self._begin[1] + self._end[1]) / 2)
        self.add_widget(load)


# Below are graphics helper classes for drawing various elements.
class Connector(Widget):
    """
    This renders a connector between two wires.
    """


class Wire(Widget):
    """
    This renders a wire.
    """


class Load(Widget):
    """
    This renders a load.
    """


class Source(Widget):
    """
    This renders the signal source.
    """


