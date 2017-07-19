#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

from circuitelement import CircuitElement

class Oscilloscope(CircuitElement):
    """
    Represents a single oscilloscope. This records any voltage passing by this
    point, with optional time controls.
    
    maxTime:        the maximum duration we record the graph, in seconds.
    minAmp:         the minimum amplitude in volts to stop recording the graph.
                    That is, if the graph rises above this value, then
                    subsequently falls below this value, we will stop recording
                    the graph. Note that this compares with the absolute value 
                    of voltage recorded.
    maxWaves:       the maximum number of waves we record. A wave is defined as
                    a rise and fall above minWaveAmp value.
    minWaveAmp:     the minimum amplitude of which we consider a section a wave.
    checkTime:      whether recording stops after maxTime.
    checkWaves:     whether recording stops after maxWaves number of waves.
    checkMinAmp:    whether recording stops after minimum amplitude has been
                    reached.
    """
    
    def __init__(self):
        """
        Initializes this resistor with given ohm value.
        """
        super(Oscilloscope, self).__init__()
        
        self._graph = ([], [])
        
        self.checkTime = True
        self.checkWaves = False
        self.checkMinAmp = False
        
        self.maxTime = 50e-9
        self.minAmp = 0.1
        self.maxWaves = 5
        self.minWaveAmp = 0.5
        
        self._maxAmp = 0
        self._waveCount = 0
        self._maxWaveAmp = 0
        
        self._isRecording = True
    
    
    @property
    def next(self):
        return self._next


    @next.setter
    def next(self, value):
        # Overriding to ignore length since oscilloscope has no length.
        self._next = value


    @property
    def prev(self):
        return self._prev


    @prev.setter
    def prev(self, value):
        self._prev = value


    def record(self, time, voltage):
        """
        Records the given time and voltage. Checks if end recording condition
        has been met.
        """
        
        amp = abs(voltage)
        
        # Check duration
        if self.checkTime and time > self.maxTime:
            self._isRecording = False
        
        # Check min amplitude
        if self.checkMinAmp:
            self._maxAmp = max(self._maxAmp, amp)
            
            if self._maxAmp > self.minAmp and amp < self.minAmp:
                self._isRecording = False
        
        # Check waves
        if self.checkWaves:
            self._maxWaveAmp = max(self._maxWaveAmp, amp)
            
            if self._maxWaveAmp > self.minWaveAmp and amp < self.minWaveAmp:
                self._waveCount += 1
                self._maxWaveAmp = amp
            
            if self._waveCount >= self.maxWaves:
                self._isRecording = False
        
        if not self._isRecording:
            return
        
        self._graph[0].append(time)
        self._graph[1].append(voltage)
        