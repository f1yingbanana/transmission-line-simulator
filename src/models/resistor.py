#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

class Resistor(CircuitElement):
    """
    Represents a single resistor. A cable can also be thought as a resistor.
    
    resistance: the value of the electrical resistance in ohms.
    """
    
    def __init__(self, ohm):
        """
        Initializes this resistor with given ohm value.
        """
        super(Resistor, self).__init__()
        
        self.resistance = ohm