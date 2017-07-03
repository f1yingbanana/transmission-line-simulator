#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement
from scipy import signal
from util.constants import *

class WaveShape:
    """
    Enumeration listing the available wave shapes.
    Gauss:
    """
    Gaussian, Triangle, Square = range(3)


class PowerSource(CircuitElement):
    """
    Represents a power supply.
    
    amplitude:  the maximum wave voltage, in volts.
    shape:      the shape of the wave.
    width:      the width of the shape, in meters.
    """
    
    def __init__(self, amplitude, resistance, width, totalWidth):
        """
        Initializes this power supply with given power and resistance.
        """
        super(PowerSource, self).__init__()
        
        self.resistance = resistance
        self.amplitude = amplitude
        self.width = width
        self.totalWidth = totalWidth
        self.shape = WaveShape.Gaussian
    
    @property
    def shape(self):
        return self._shape
    
    @shape.setter
    def shape(self, value):
        self._shape = value
        
        points = int(self.width / self.totalWidth * DISCRETE_STEPS)
        
        if value == WaveShape.Gaussian:
            self._output = signal.gaussian(points, self.width * 10.0).tolist()
        elif value == WaveShape.Square:
            self._output = [1] * points
        elif value == WaveShape.Triangle:
            self._output = []
            
            for i in range(points / 2):
                self._output.append(i * 2.0 / points)
            
            for i in range(points / 2):
                self._output.append(1 - i * 2.0 / points)
    
    
    def getOutput(self):
        if len(self._output) == 0:
            return 0
        else:
            return self._output.pop(0) * self.amplitude
        