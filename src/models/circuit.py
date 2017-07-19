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
        source = PowerSource(10.0, 5.0, 1, 5.0)
        source.getLength = self.getLength
        cable = Resistor(5.0)
        cable2 = Resistor(10.0)
        load = Resistor(0.0)
        cable.length = 2.5
        cable2.length = 2.5
        source.next = cable
        cable.next = cable2
        cable2.next = load
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

        if self.headOscilloscope == None:
            self.headOscilloscope = o
            return

        h = self.headOscilloscope

        while h != None:
            if h.position > o:
                if h.prev != None:
                    h.prev.next = o

                o.prev = h.prev
                h.prev = o
                o.next = h

                break

            h = h.next
        
        return o
        

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

