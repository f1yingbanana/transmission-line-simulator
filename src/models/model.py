#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from util.constants import *
from collections import deque
from circuit import Circuit

class AppState(object):
    """
    Describes the valid states in this app.
    """
    Editing, Simulating = range(2)


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
    appState:           the application state.
    """
    
    
    def __init__(self):
        """
        Initializes a brand new model for a fresh app start.
        """
        self.forwardCurrent = deque([0] * (DISCRETE_STEPS + 1))
        self.backwardCurrent = deque([0] * (DISCRETE_STEPS + 1))
        self.overallDistribution = [0] * (DISCRETE_STEPS + 1)
        self.circuit = Circuit()
        self.waveSpeed = 299792458
        self.simSpeed = 1e-9
        self._elapsed = 0
        self._lastStep = 0
        self.appState = AppState.Editing
    
    
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
            self._step()
        
        # Update every oscilloscope
        scopes = self.circuit.getOscilloscopes()
        
        for scope in scopes:
            i = int(DISCRETE_STEPS * scope.position / l)
            v = self.forwardCurrent[i] + self.backwardCurrent[i]
            scope.record(self._elapsed, v)
    
    
    def _step(self):
        """
        Simulates a discrete step for each part of the circuit.
        """
        self._lastStep = self._elapsed
        
        # We go through each discretized value in forward and backward
        # currents, deciding whether it should move or not, and how it
        # should move.
        l = self.circuit.getLength()
        
        for i in range(DISCRETE_STEPS + 1):
            # Check if this segment contains a resistor. If so, we need
            # to do a reflection.
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
        v = self.circuit.head.getOutput()
        self.forwardCurrent[0] = v
        self.backwardCurrent[-1] = 0
        
        # Recompute overall
        for i in range(len(self.forwardCurrent)):
            # print '[' + str(self.forwardCurrent[i]) + ', ' + \
            # str(self.backwardCurrent[i]) + ']'
            v = self.forwardCurrent[i] + self.backwardCurrent[i]
            self.overallDistribution[i] = v
