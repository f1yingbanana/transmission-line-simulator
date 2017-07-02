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
                attached to it.
    next:       the next connected circuit element, in current direction order.
    prev:       the previous connected circuit element, in current direction
                order.
    """
    
    def __init__(self):
        self.position = 0
        self.next = None
        self.prev = None