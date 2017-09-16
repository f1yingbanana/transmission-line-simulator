#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement
import util.signal as signal
from util.constants import *
import numpy as np

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
    width:      the width of the shape, in ns (that is, width is actually how
                long the wave will be emitted).
    """
    
    def __init__(self, amplitude, impedance, width):
        """
        Initializes this power supply with given power and impedance.
        """
        super(PowerSource, self).__init__()
        
        self.impedance = impedance
        self._amplitude = amplitude
        self._width = width
        self.shape = WaveShape.Gaussian
    
    
    @property
    def shape(self):
        return self._shape
    
    
    @shape.setter
    def shape(self, value):
        self._shape = value
        
        points = int(self.width * STEPS_PER_NS)
        
        if value == WaveShape.Gaussian:
            # We want to have value 1/e at +-(points-1)/2. But we want to have
            # some more points at both ends to produce smoother graph. So.
            self.forward = signal.gaussian(3 * points, points / 2.0 / 2 ** 0.5)
        elif value == WaveShape.Square:
            self.forward = np.ones(points)
        elif value == WaveShape.Triangle:
            self.forward = np.concatenate(np.arange(0, 1, 2.0 / points), np.arange(1, 0, 2.0 / points))

        self.forward *= self.amplitude


    @property
    def amplitude(self):
        return self._amplitude


    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = value
        self.shape = self.shape


    @property
    def width(self):
        return self._width


    @width.setter
    def width(self, value):
        self._width = value
        self.shape = self.shape


    def reset(self):
        """
        Resets the power source, allowing it to output a fresh wave.
        """
        self.shape = self.shape


    def split(self):
        """
        Reduces the voltage to match the first wire connected to the source.
        """
        t = float(self.next.impedance) / (self.impedance + self.next.impedance)
        self.forward[-1] *= t


    def rotateForward(self):
        """
        Pops the last value and replace with 0.
        """
        self.forward = np.roll(self.forward, 1)
        self.forward[0] = 0

