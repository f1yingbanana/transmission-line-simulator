#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-27-2017
#

from util.constants import *
from circuitelement import CircuitElement
import numpy as np

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
        super(Wire, self).__init__()
        
        self.impedance = ohm
        self.speed = speed


    def split(self):
        # Splitting forward
        amp = self.forward[-1]
        r = self.next.impedance
        z = self.impedance
        reflCoefficient = (r - z) / (r + z)
        self.forward[-1] -= reflCoefficient * amp
        self.backward[-1] += reflCoefficient * amp
        
        # Splitting backward
        amp = self.backward[0]
        r = self.prev.impedance
        z = self.impedance
        reflCoefficient = (r - z) / (r + z)
        self.backward[0] -= reflCoefficient * amp
        self.forward[0] += reflCoefficient * amp
        

    def rotateForward(self):
        self.forward = np.roll(self.forward, 1)
        self.forward[0] = self.prev.forward[-1]
        

    def rotateBackward(self):
        self.backward = np.roll(self.backward, -1)
        self.backward[-1] = self.next.backward[0]
