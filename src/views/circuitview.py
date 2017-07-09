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
from util.constants import *
from util.hoverbehavior import HoverBehavior
from source import Source
from kivy.core.window import Window


class CircuitWidget(Widget, HoverBehavior):
    """
    Base widget for circuit element, supporting functions like highlighting,
    editing hooks and right click menu hooks.
    """
    def __init__(self, **kwargs):
        super(CircuitWidget, self).__init__(**kwargs)


    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            if touch.button == 'left':
                self.on_left_click()
            elif touch.button == 'right':
                self.on_right_click()

            return True

        return super(CircuitWidget, self).on_touch_down(touch)

    def on_left_click(self):
        print 'editing element!'

    def on_right_click(self):
        print 'generating menu!'

    def on_enter(self):
        print 'hovering'

    def on_leave(self):
        print 'left'



# Below are graphics helper classes for drawing various elements.
class Connector(CircuitWidget):
    """
    This renders a connector between two wires.
    """


class Wire(CircuitWidget):
    """
    This renders a wire.
    """


class Load(CircuitWidget):
    """
    This renders a load.
    """

class Source(CircuitWidget):
    """
    This renders a power source.
    """


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
        bx, by = box[0], self.y + self.height * 0.2
        ex, ey = box[0] + box[2], self.y + self.height * 0.8

        if abs(bx - self._begin[0]) < 1e-7 and \
            abs(by - self._begin[1]) < 1e-7 and \
            abs(ex - self._end[0]) < 1e-7 and \
            abs(ey - self._end[1]) < 1e-7:
            return

        self._begin = bx, by
        self._end = ex, ey
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
                c.size = 2 * WIRE_THICKNESS, 2 * WIRE_THICKNESS + 48
                c.center = float(self._begin[0] + e.position * scale), self._end[1]
                self.add_widget(c)
                needConnector = False

            # This element is either a wire or oscilloscope.
            if type(e) == Resistor:
                needConnector = True
                w = Wire()
                w.x = float(self._begin[0] + e.position * scale + WIRE_THICKNESS)
                w.width = float(max(0, e.length * scale - 2 * WIRE_THICKNESS))
                w.height = 2 * WIRE_THICKNESS + 48
                w.center_y = self._end[1]
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
