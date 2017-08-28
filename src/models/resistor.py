#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement

class Resistor(CircuitElement):
    """
    Represents a single resistor. This class allows some clarification on
    difference between resistor and oscilloscope.
    """
    
    def __init__(self, ohm):
        """
        Initializes this resistor with given ohm value.
        """
        super(Resistor, self).__init__()
        
        self.impedance = ohm