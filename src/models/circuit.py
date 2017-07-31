#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement
from powersource import PowerSource
from resistor import Resistor
from oscilloscope import Oscilloscope
from util.constants import *
from wire import Wire

class Circuit(object):
    """
    An instance that describes exactly how the circuit is set up. A circuit
    consists of a list of resistors connected in series or in parallel.
    
    head:   the first element of the circuit. This is a linked list.
    """
    
    def __init__(self):
        """
        Initializes a brand new circuit with a power source, single cable and a
        single load at the right.
        """
        source = PowerSource(10.0, 5.0, 1)
        cable = Wire(5.0, 1)
        load = Resistor(0.0)
        cable.length = 5.0
        source.next = cable
        cable.next = load
        self.head = source
        self.headOscilloscope = None
    

    def getLength(self):
        """
        Calculates and returns the length going from the power source to the
        load on the right, in meters.
        """
        p = 0
        e = self.head
        
        while e != None:
            p = e.position
            e = e.next
        
        return p
    
    
    def insertOscilloscope(self, pos):
        """
        Inserts a new oscilloscope at given circuit position. Returns the
        inserted item.
        """
        pos = max(0, min(self.getLength(), pos))

        o = Oscilloscope()
        o.position = pos
        self._insert(o)

        return o


    def splitWire(self, e, pos):
        c = Wire(e.impedance, e.speed)
        c.length = e.length - pos
        c.next = e.next
        e.length = pos
        e.next = c

        # Now reset oscilloscopes' wire properties.
        o = self.headOscilloscope

        while o != None:
            if e.position <= o.position and e.position + e.length >= o.position:
                o.wire = e
            elif c.position <= o.position and c.position + c.length >= o.position:
                o.wire = c
        
            o = o.next


    def deleteWire(self, element):
        element.prev.next = element.next

        # Delete any oscilloscopes on this segment, and also changes positioning
        # for later oscilloscopes.
        h = self.headOscilloscope

        while h != None:
            if h.position > element.position:
                if h.position < element.position + element.length:
                    # Delete oscilloscope.
                    if h.prev != None:
                        h.prev.next = h.next

                    if h.next != None:
                        h.next.prev = h.prev

                    if h == self.headOscilloscope:
                        self.headOscilloscope = h.next
                else:
                    # Move oscilloscope.
                    h.position -= element.length

            h = h.next


    def moveOscilloscope(self, element, pos):
        """
        Moves the given oscilloscope to somewhere else.
        """
        element.position = pos

        # First detach
        if element.prev != None:
            element.prev.next = element.next

        if element.next != None:
            element.next.prev = element.prev

        if self.headOscilloscope == element:
            self.headOscilloscope = element.next

        # Now reinsert
        self._insert(element)


    def checkOscilloscopes(self):
        # Checks and removes out of bound osclloscopes.
        o = self.headOscilloscope
        l = self.getLength()

        while o != None:
            if o.position > l:
                if o.prev != None:
                    o.prev.next = None
                elif o == self.headOscilloscope:
                    self.headOscilloscope = None

            o = o.next


    def _insert(self, o):
        # First determine wire
        e = self.head.next

        while e.next != None:
            if e.position <= o.position and e.position + e.length >= o.position:
                break

            e = e.next

        o.wire = e

        # Now insert into linked list.
        if self.headOscilloscope == None:
            self.headOscilloscope = o
            return

        h = self.headOscilloscope

        while h != None:
            if h.position > o.position:
                if h.prev != None:
                    h.prev.next = o
                else:
                    self.headOscilloscope = o

                o.prev = h.prev
                h.prev = o
                o.next = h

                return
            elif h.next == None:
                h.next = o
                o.prev = h

                break

            h = h.next


    def getElements(self, position, isForward):
        """
        Returns the circuit elements positioned at the given position.
        
        position:   the discretized position along the circuit, in meters.
        isForward:  whether we are looking for junctions of elements going
                    forward.
        """
        es = []
        
        e = self.head

        step = self.getLength() / DISCRETE_STEPS
        
        while e != None:
            if isForward:
                if position <= e.position and e.position < position + step:
                    es.append(e)
            else:
                if position >= e.position + e.length and e.position > position + e.length - step:
                    es.append(e)
            
            e = e.next
        
        if not isForward:
            es.reverse()
        
        return es


    def reset(self):
        e = self.head

        while e != None:
            e.reset()
            e = e.next

        e = self.headOscilloscope

        while e != None:
            e.reset()
            e = e.next
