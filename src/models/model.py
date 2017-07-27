#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

from util.constants import *
from collections import deque
from circuit import Circuit
import numpy as np

class AppState(object):
    """
    Describes the valid states in this app.
    """
    Editing = 'editing'
    Simulating = 'simulating'
    Paused = 'paused'


class Model(object):
    """
    An instance that keeps data on the simulation, including circuit info,
    wave generation, animations, and so on.
    
    circuit:            model representing the current state of electrical
                        components in the system.
    waveSpeed:          speed of wave, in m/s.
    simSpeed:           simulation speed, a multiplier for elapsed time.
    appState:           the application state.
    elapsed:            amount of elapsed time, in seconds.
    maxAmplitude:       the maximum amplitude reached within the current 
                        simulation.
    """
    
    
    def __init__(self):
        """
        Initializes a brand new model for a fresh app start.
        """
        self.graph = [np.array([]), np.array([])]
        self.circuit = Circuit()
        self.simSpeed = 1.0 / NS_IN_S
        self.elapsed = 0
        self._lastStep = 0
        self.maxAmplitude = 10
        self.appState = AppState.Editing
    
    
    def simulate(self, dt):
        """
        Simulate the system by step dt, in seconds.
        """
        last = self.elapsed
        self.elapsed += dt * self.simSpeed
        
        # Determine how many steps must be made.
        segs = int(STEPS_PER_NS * (self.elapsed - self._lastStep) * NS_IN_S)
        
        for s in range(segs):
            self._lastStep += 1.0 / STEPS_PER_NS / NS_IN_S
            self._step()

            # Recompute overall
            self.graph = [np.array([]), np.array([])]
            e = self.circuit.head.next

            while e.next != None:
                self.graph[0] = np.concatenate((self.graph[0], e.xs))
                v = e.forward + e.backward

                if len(v) > 0:
                    self.maxAmplitude = max(self.maxAmplitude, v.max(), v.min())

                self.graph[1] = np.concatenate((self.graph[1], v))
                e = e.next

            # Update every oscilloscope
            h = self.circuit.headOscilloscope

            i = 0
            
            while h != None:
                if i >= len(self.graph[0]):
                    break

                while self.graph[0][i] < h.position:
                    i += 1

                h.record(self._lastStep, self.graph[1][i - 1])
                h = h.next


    def reset(self):
        """
        Resets the simulation, but not the circuit.
        """
        self.elapsed = 0
        self._lastStep = 0
        self.graph = [np.array([]), np.array([])]
        self.circuit.reset()
        self.maxAmplitude = 10


    def _step(self):
        """
        Simulates a discrete step for each part of the circuit.
        """
        
        # We go through each discretized value in forward and backward
        # currents, deciding whether it should move or not, and how it
        # should move.
        e = self.circuit.head

        while e != None:
            e.split()
            e = e.next

        # Now shift
        e = self.circuit.head

        while e.next != None:
            e.rotateBackward()
            e = e.next

        while e != None:
            e.rotateForward()
            e = e.prev
