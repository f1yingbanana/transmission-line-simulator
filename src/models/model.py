#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from util.constants import *
from collections import deque
from circuit import Circuit

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
        self.forwardCurrent = deque([0] * (DISCRETE_STEPS + 1))
        self.backwardCurrent = deque([0] * (DISCRETE_STEPS + 1))
        self.circuit = Circuit()
        self.waveSpeed = 299792458
        self.simSpeed = 1e-9
        self._elapsed = 0
        self._lastStep = 0
        
        print self.getVoltageDistribution()
    
    
    def simulate(self, dt):
        """
        Simulate the system by step dt, in seconds.
        """
        self._elapsed += dt * self.simSpeed
        
        # Determine how many steps must be made.
        l = self.circuit.getLength()
        dx = l / DISCRETE_STEPS
        
        segs = int((self._elapsed - self._lastStep) * self.waveSpeed / dx)
        
        
        
        for s in range(segs):
            print "stepping"
            self._step()
            print self.getVoltageDistribution()
        
        # Update every oscilloscope
        # TODO
    
    
    def getVoltageDistribution(self):
        """
        Returns the overall voltage distribution across the wire, as divided
        into DISCRETE_STEPS.
        """
        l = []
        
        for i in range(len(self.forwardCurrent)):
            l.append(self.forwardCurrent[i] + self.backwardCurrent[i])
        
        return l
    
    
    def _step(self):
        """
        Simulates a discrete step for each part of the circuit.
        """
        self._lastStep = self._elapsed
        
        # We go through each discretized value in forward and backward
        # currents, deciding whether it should move or not, and how it
        # should move.
        for i in range(DISCRETE_STEPS + 1):
            # Check if this segment contains a resistor. If so, we need
            # to do a reflection.
            l = self.circuit.getLength()
            es = self.circuit.getElements(i * l / DISCRETE_STEPS, True)
            fwd = self.forwardCurrent[i]
            bwd = self.backwardCurrent[i]
            
            for e in es:
                if abs(self.forwardCurrent[i]) > 0 and e.prev != None:
                    # Simulate forward
                    r = e.resistance
                    z = e.prev.resistance
                    reflCoefficient = (r - z) / (r + z)
                    fwd -= reflCoefficient * self.forwardCurrent[i]
                    bwd += reflCoefficient * self.forwardCurrent[i]
            
            es = self.circuit.getElements(i * l / DISCRETE_STEPS, False)
            
            for e in es:
                if abs(self.backwardCurrent[i]) > 0 and e.next != None:
                    # Simulate backward
                    r = e.resistance
                    z = e.next.resistance
                    reflCoefficient = (r - z) / (r + z)
                    fwd += reflCoefficient * self.backwardCurrent[i]
                    bwd -= reflCoefficient * self.backwardCurrent[i]
        
            self.forwardCurrent[i] = fwd
            self.backwardCurrent[i] = bwd
        
        # Now shift
        self.forwardCurrent.rotate(1)
        self.backwardCurrent.rotate(-1)
        
        # Clear out the endpoints, but if power source is still emitting wave,
        # set it to that
        self.forwardCurrent[0] = self.circuit.head.getOutput()
        self.backwardCurrent[-1] = 0
