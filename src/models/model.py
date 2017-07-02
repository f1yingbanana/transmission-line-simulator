#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from constants import *
from collections import deque

class Model(object):
    """
    An instance that keeps data on the simulation, including circuit info,
    wave generation, animations, and so on.
    
    forwardCurrent:     a deque of discretized current values (in amps) in the
                        circuit traveling forward (going out from the power
                        source).
    backwardCurrent:    a deque of discretized current values (in amps) in the
                        circuit traveling backward (coming in to the power
                        source).
    circuit:            model representing the current state of electrical
                        components in the system.
    waveSpeed:          speed of wave, in m/s.
    simSpeed:           simulation speed, a multiplier for elapsed time.
    """
    
    
    def __init__(self):
        """
        Initializes a brand new model for a fresh app start.
        """
        self.forwardCurrent = deque([0] * DISCRETE_STEPS)
        self.backwardCurrent = deque([0] * DISCRETE_STEPS)
        self.circuit = Circuit()
        self.speed = 299792458
        self.simSpeed = 1
        self._elapsed = 0
        self._lastStep = 0
    
    
    def simulate(dt):
        """
        Simulate the system by step dt, in seconds.
        """
        self._elapsed += dt * self.simSpeed
        
        # Determine how many steps must be made.
        l = self.circuit.getLength()
        dx = l / DISCRETE_STEPS
        
        segs = (self._elapsed - self._lastStep) * self.waveSpeed / dx
        
        for s in range(segs):
            self._lastStep = self._elapsed
        
            # We go through each discretized value in forward and backward
            # currents, deciding whether it should move or not, and how it
            # should move.
            for i in range(DISCRETE_STEPS):
                # Check if this segment contains a resistor. If so, we need
                # to do a reflection.
                es = self.circuit.getElements(i * l / DISCRETE_STEPS)
                
                for e in es:
                    if type(e) == Resistor:
                        # Reflect
                        fwd = 0
                        bwd = 0
                        
                        if i > 0:
                            # Simulate forward
                            pass
                        
                        if i < DISCRETE_STEPS - 1:
                            # Simulate backward
                            pass
                        
                        self.forwardCurrent[i] = fwd
                        self.backwardCurrent[i] = bwd
                
                # Now shift
                self.forwardCurrent.rotate(1)
                self.backwardCurrent.rotate(1)
