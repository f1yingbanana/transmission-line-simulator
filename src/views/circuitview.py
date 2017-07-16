#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-9-2017
#

from kivy.uix.widget import Widget
from materialwidget import MaterialWidget
from materialtextfield import MaterialTextField
from kivy.properties import *
from models.resistor import Resistor
from models.oscilloscope import Oscilloscope
from util.constants import *
from util.hoverbehavior import HoverBehavior
from kivy.core.window import Window
from contextmenu import ContextMenu
from models.circuit import Circuit
from loadeditor import LoadEditor
from wireeditor import WireEditor
from sourceeditor import SourceEditor
from kivy.metrics import *

class CircuitWidget(Widget, HoverBehavior):
    """
    Base widget for circuit element, supporting functions like highlighting,
    editing hooks and right click menu hooks.
    """
    def __init__(self, **kwargs):
        super(CircuitWidget, self).__init__(**kwargs)

        self.contextMenuLayer = None
        self.element = None
        self.updateCircuit = None
        self._menuPos = 0
        self.wireScale = 0
        self.menu = None


    def on_touch_down(self, touch):
        if self.collide_point(touch.pos[0], touch.pos[1]):
            self._menuPos = touch.pos

            if touch.button == 'left':
                self.on_left_click(touch.pos)
            elif touch.button == 'right':
                self.on_right_click(touch.pos)

            return True

        return super(CircuitWidget, self).on_touch_down(touch)


    def on_left_click(self, pos):
        self.onEditClicked()


    def on_right_click(self, pos):
        if self.menu == None:
            return

        if self.menu.parent != None:
            self.menu.dismiss(False)
        
        self.menu.show(self.contextMenuLayer, pos, True)


    def onEditClicked(self):
        self.popup.updateCircuit = self.updateCircuit

        if self.popup.parent != None:
            self.popup.dismiss(False)
        
        self.popup.show(self.contextMenuLayer, self._menuPos, True)
        self.popup.updateValues()


    def onNext(self):
        """
        Opens the next menu
        """
        self.popup.dismiss(False)
        self.next._menuPos = self.next.center
        self.next.onEditClicked()


    def onPrev(self):
        """
        Opens the next menu
        """
        self.popup.dismiss(False)
        self.prev._menuPos = self.prev.center
        self.prev.onEditClicked()


class Wire(CircuitWidget):
    """
    This renders a wire.
    """
    def __init__(self, wireModel, **kwargs):
        super(Wire, self).__init__(**kwargs)

        self.element = wireModel
        titles = ['Edit Wire', 'Split Wire'] #, 'Add Monitor']
        actions = [self.onEditClicked, self.onSplitClicked] #, self.onAddMonitorClicked]

        if self._canDelete():
            titles.append('Delete Wire')
            actions.append(self.onDeleteClicked)

        self.menu = ContextMenu(titles, actions)
        self.popup = WireEditor(self.element)
        self.popup.onPrev = self.onPrev
        self.popup.onNext = self.onNext


    def _canDelete(self):
        return self.element.prev.prev != None or self.element.next.next != None


    def onSplitClicked(self):
        """
        Splits the wire at the menu pos, cutting it in two identical halves.
        """
        wirePos = (self._menuPos[0] - self.x) / self.wireScale
        # Discretize the above.

        copy = Resistor(self.element.resistance)
        copy.length = self.element.length - wirePos
        copy.next = self.element.next
        self.element.length = wirePos
        self.element.next = copy
        self.rebuild()


    def onAddMonitorClicked(self):
        pass


    def onDeleteClicked(self):
        self.element.prev.next = self.element.next
        self.rebuild()



class Load(CircuitWidget):
    """
    This renders a load.
    """
    def __init__(self, loadModel, **kwargs):
        super(Load, self).__init__(**kwargs)

        titles = ['Edit Load', 'Reset Circuit']
        actions = [self.onEditClicked, self.onResetClicked]
        self.menu = ContextMenu(titles, actions)
        self.element = loadModel
        self.popup = popup = LoadEditor(self.element)
        self.popup.onPrev = self.onPrev


    def onResetClicked(self):
        self.resetCircuit()


class Source(CircuitWidget):
    """
    This renders a power source.
    """
    def __init__(self, element, **kwargs):
        super(Source, self).__init__(**kwargs)

        titles = ['Edit Source', 'Reset Circuit']
        actions = [self.onEditClicked, self.onResetClicked]
        self.menu = ContextMenu(titles, actions)
        self.element = element
        self.popup = SourceEditor(self.element)
        self.popup.onNext = self.onNext


    def onResetClicked(self):
        self.resetCircuit()


class CircuitView(MaterialWidget):
    """
    This is dedicated in displaying and editing the circuit.

    model:  the simulation model.
    """

    _begin = ListProperty([0, 0])
    _end = ListProperty([0, 0])

    model = ObjectProperty(None)

    contextMenuLayer = ObjectProperty(None)


    def __init__(self, **kwargs):
        """
        Initializes the view without drawing anything.
        """
        super(CircuitView, self).__init__(**kwargs)
    

    def on_model(self, *args, **kwargs):
        self.rebuildCircuit()


    def setGraphBounds(self, box):
        """
        This takes the graph positions and aligns itself with the graph.

        box:    a bounding box in the format of [x, y, width, height]
        """
        bx, by = box[0], self.y + 80
        ex, ey = box[0] + box[2], self.y + self.height - 80

        if abs(bx - self._begin[0]) < 1e-7 and \
            abs(by - self._begin[1]) < 1e-7 and \
            abs(ex - self._end[0]) < 1e-7 and \
            abs(ey - self._end[1]) < 1e-7:
            return

        self._begin = bx, by
        self._end = ex, ey
        self.rebuildCircuit()


    def resetCircuit(self):
        self.model.reset()
        self.model.circuit = Circuit()


    def updateCircuit(self):
        """
        Updates the length of all the wires in the diagram and also positioning
        of oscilloscopes.
        """
        scale = (self._end[0] - self._begin[0]) / self.model.circuit.getLength()
        lastX = 0

        for c in self.children:
            if type(c) == Wire:
                c.x = float(self._begin[0] + c.element.position * scale + WIRE_THICKNESS)
                c.width = float(max(0, c.element.length * scale - 2 * WIRE_THICKNESS))
                lastX = c.x + c.element.position


    def rebuildCircuit(self):
        """
        Removes all circuit elements from the diagram and add everything from
        model.
        """
        if self.model == None:
            return

        self.clear_widgets()

        # Add a source.
        source = Source(self.model.circuit.head)
        source.contextMenuLayer = self.contextMenuLayer
        source.resetCircuit = self.resetCircuit
        source.size = dp(40), dp(40)
        source.center = float(self._begin[0]), float((self._begin[1] + self._end[1]) / 2)
        self.add_widget(source)

        # Add each wire and oscilloscpe with a connector inbetween.
        e = self.model.circuit.head.next
        scale = (self._end[0] - self._begin[0]) / self.model.circuit.getLength()
        c = None

        p1 = source
        p2 = source

        while e.next != None:
            # This element is either a wire or oscilloscope.
            if type(e) == Resistor:
                needConnector = True

                w = Wire(e)
                w.wireScale = scale
                w.updateCircuit = self.updateCircuit
                w.rebuild = self.rebuildCircuit
                w.contextMenuLayer = self.contextMenuLayer
                w.x = float(self._begin[0] + e.position * scale + WIRE_THICKNESS)
                w.width = float(max(0, e.length * scale - 2 * WIRE_THICKNESS))
                w.height = 2 * WIRE_THICKNESS + 48
                w.center_y = self._begin[1]

                w.prev = p1
                w.prev.next = w
                p1 = w

                self.add_widget(w)

                w = Wire(e)
                w.wireScale = scale
                w.updateCircuit = self.updateCircuit
                w.rebuild = self.rebuildCircuit
                w.contextMenuLayer = self.contextMenuLayer
                w.x = float(self._begin[0] + e.position * scale + WIRE_THICKNESS)
                w.width = float(max(0, e.length * scale - 2 * WIRE_THICKNESS))
                w.height = 2 * WIRE_THICKNESS + 48
                w.center_y = self._end[1]

                w.prev = p2
                w.prev.next = w
                p2 = w

                self.add_widget(w)
            elif type(e) == Oscilloscope:
                pass
            
            # Proceed to the next element
            e = e.next

        # Add a load.
        load = Load(e)
        load.contextMenuLayer = self.contextMenuLayer
        load.resetCircuit = self.resetCircuit
        load.size = 40, 120
        load.center = float(self._end[0]), float((self._begin[1] + self._end[1]) / 2)
        load.prev = p1
        p1.next = load
        p2.next = load
        self.add_widget(load)
