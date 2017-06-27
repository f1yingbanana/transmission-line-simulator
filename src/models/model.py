#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

"""
This module contains the model classes for the transmission line simulation. 
"""

from constants import *

class Model(object):
    """
    An instance that keeps data on the simulation, including circuit info,
    wave generation, animations, and so on.
    
    forwardCurrent:     a list of discretized current values (in amps) in the
    circuit traveling forward (going out from the power source).
    backwardCurrent:    a list of discretized current values (in amps) in the
    circuit traveling backward (coming in to the power source).
    circuit:            model representing the current state of electrical
                        components in the system.
    """
    
    
    def __init__(self):
        """
        Initializes a brand new model for a fresh app start.
        """
        self.forwardCurrent = [0] * DISCRETE_STEPS
        self.backwardCurrent = [0] * DISCRETE_STEPS
        self.circuit = Circuit()
        self._elapsed = 0
    
    def simulate(dt):
        """
        Simulate the system by step dt, in seconds.
        """
        self._elapsed += dt
        
        # We go through each discretized value in forward and backward currents,
        # deciding whether it should move or not, and how it should move.
        for i in range(DISCRETE_STEPS):
            # Simulate the ith forward segment.
            amp = self.forwardCurrent[i]
            
            # Simulate the ith backward segment.
            amp = self.backwardCurrent[i]
        


class Circuit(object):
    """
    An instance that describes exactly how the circuit is set up. A circuit
    consists of a list of resistors connected in series or in parallel.
    """
    def __init__(self):
        """
        Initializes a brand new circuit with a power source, standard lines and
        a single load at the right.
        """
        self.elements = []
    
    def getLength(self):
        """
        Calculates and returns the length going from the power source to the
        load on the right.
        """
        # Just sum up all the wires' lengths.
        return 10
    
    

class CircuitElement(object):
    """
    An abstract class that contains basic information on elements on a circuit.
    """

class Resistor(CircuitElement):
    """
    Represents a single resistor. A cable can also be thought as a resistor.
    
    resistance: the value of the electrical resistance in ohms.
    """
    
    def __init__(self, ohm):
        """
        Initializes this resistor with given ohm value.
        """
        self.resistance = ohm