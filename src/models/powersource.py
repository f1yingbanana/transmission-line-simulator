#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement


class WaveShape:
    """
    Enumeration listing the available wave shapes.
    Gauss:
    """
    Gauss, Triangle, Square = range(3)


class PowerSource(CircuitElement):
    """
    Represents a power supply.
    
    power:  the maximum wave voltage, in volts.
    shape:  the shape of the wave.
    """
    
    def __init__(self, amplitude, resistance):
        """
        Initializes this power supply with given power and resistance.
        """
        super(PowerSource, self).__init__()
        
        self.resistance = resistance
        self.amplitude = amplitude
        self.shape = WaveShape.Gauss
        
        self._output = [1, 4, 9, 16, 9, 4, 1]
    
    
    def getOutput(self):
        if len(self._output) == 0:
            return 0
        else:
            return self._output.pop(0)
