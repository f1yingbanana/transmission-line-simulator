#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

class Circuit(object):
    """
    An instance that describes exactly how the circuit is set up. A circuit
    consists of a list of resistors connected in series or in parallel.
    
    elements:   a sorted list of circuit elements by position.
    """
    
    def __init__(self):
        """
        Initializes a brand new circuit with a power source, single cable and a
        single load at the right.
        """
        self.elements = []
    
    
    def getLength(self):
        """
        Calculates and returns the length going from the power source to the
        load on the right, in meters.
        """
        # Just sum up all the wires' lengths.
        return 10.0
    
    
    def getElements(self, position):
        """
        Returns the circuit elements positioned at the given position. This
        search assumes position is discretized through DISCRETE_STEPS in module
        'constants'.
        
        position:   the discretized position along the circuit, in meters. 
        """
        es = []
        
        for e in self.elements:
            if e.position == position:
                es += e
        
        return es
