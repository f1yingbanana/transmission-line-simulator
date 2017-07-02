#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

class Oscilloscope(CircuitElement):
    """
    Represents a single oscilloscope. This records any voltage passing by this
    point, with optional time controls.
    
    maxTime:    the maximum duration we record the graph, in seconds.
    minAmp:     the minimum amplitude in wave to stop recording the graph. That
    is, we first need to record a voltage higher than this value, then stop 
    recording when it drops below this value. In volts.
    maxWaves:   the maximum number of waves we record. A wave is defined as a
    rise and fall above minAmp voltage value.
    """
    
    def __init__(self):
        """
        Initializes this resistor with given ohm value.
        """
        super(Oscilloscope, self).__init__()
        
        self._graph = []
        
        self.maxTime = 50e-9
        self.minAmp = 0.1
        self.maxWaves = float('inf')
        