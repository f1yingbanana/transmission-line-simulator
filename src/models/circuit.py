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
    
    
    def getOscilloscopes(self):
        """
        Returns all oscilloscopes in the circuit.
        """
        es = []
        
        e = self.head
        
        while e != None:
            if type(e) == Oscilloscope:
                es.append(e)
            
            e = e.next
        
        return es
    
    
    def getElements(self, position, isForward):
        """
        Returns the circuit elements positioned at the given position. This
        search assumes position is discretized through DISCRETE_STEPS in module
        'constants'.
        
        position:   the discretized position along the circuit, in meters.
        isForward:  whether we are looking for junctions of elements going
                    forward.
        """
        es = []
        
        e = self.head
        
        while e != None:
            if isForward:
                if abs(e.position - position) <= 1e-7:
                    es.append(e)
            else:
                if abs(e.position + e.length - position) <= 1e-7:
                    es.append(e)
            
            e = e.next
        
        if not isForward:
            es.reverse()
        
        return es
        


