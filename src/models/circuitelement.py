#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

class CircuitElement(object):
    """
    An abstract class that contains basic information on elements on a circuit.
    
    position:   the position of this circuit element along the circuit. This is
                the starting position of the element, if there is any length
                attached to it, in meters.
    length:     the length of this circuit element along the circuit, in meters.
    next:       the next connected circuit element, in current direction order.
    prev:       the previous connected circuit element, in current direction
                order.
    resistance: the total resistance of the element, in ohms.
    """
    
    def __init__(self):
        self.position = 0
        self.length = 0
        self.next = None
        self.prev = None
        self.resistance = 0