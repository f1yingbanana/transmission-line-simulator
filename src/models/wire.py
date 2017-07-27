#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-27-2017
#

from circuitelement import CircuitElement

class Wire(CircuitElement):
    """
    Represents a wire. This class allows an arbitrary signal speed and relays
    voltage accordingly.
    """
    
    def __init__(self, ohm, speed):
        """
        Initializes this wire with given ohm value and speed.

        ohm:    impedence in ohms.
        speed:  speed of wave propagation in c.
        """
        super(Resistor, self).__init__()
        
        self.impedance = ohm
        self.speed = speed