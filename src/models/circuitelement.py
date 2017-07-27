#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

import numpy as np
from util.constants import *

class CircuitElement(object):
    """
    An abstract class that contains basic information on elements on a circuit.
    
    position:   the position of this circuit element along the circuit. This is
                the starting position of the element, if there is any length
                attached to it, in meters.
    length:     the length of this circuit element along the circuit, in meters.
    next:       the next connected circuit element, in current direction order.
    prev:       the previous connected circuit element, in current direction
                order.
    impedance:  the impedance of the element, in ohms.
    forward:    ndarray of discretized voltage (in V) in the element traveling 
                forward (going out from the power source).
    backward:   ndarray of discretized voltage (in V) in the element traveling 
                forward (going into the power source).
    xs:         the x coordinates of the discretized points in forward and
                backward arrays.
    speed:      how fast the wave propagates in this element in units of c.
    """
    
    def __init__(self):
        self._position = 0
        self._length = 0
        self._speed = 1
        self._next = None
        self._prev = None
        self.impedance = 0
        self.forward = np.array([])
        self.backward = np.array([])
        self.xs = np.array([])


    def split(self):
        """
        Split the amplitude into forward and backward at the edge of the
        element.
        """
        pass


    def rotateForward(self):
        """
        Rotate every stored forward amplitude in the element.
        """
        pass


    def rotateBackward(self):
        """
        Rotate every stored backward amplitude in the element.
        """
        pass


    @property
    def speed(self):
        return self._speed


    @speed.setter
    def speed(self, value):
        """
        We set the speed and then expand / shrink our inernal representation of
        forward and backward amplitude lists.
        """
        self._speed = max(1e-8, min(1, value))
        self._updateArrays()


    @property
    def next(self):
        return self._next


    @next.setter
    def next(self, value):
        # When setting the next element, we update that element and everything
        # after it their position.
        self._next = value

        if value != None:
            value._prev = self
            value.position = self.position + self.length

            nxt = value.next

            while nxt != None:
                nxt.position = value.position + value.length
                value = nxt
                nxt = nxt.next


    @property
    def prev(self):
        return self._prev


    @prev.setter
    def prev(self, value):
        self._prev = value

        if value != None:
            value._next = self
            value.position = self.position - value.length

            prv = value.prev

            while prv != None:
                prv.position = value.position - prv.length
                value = prv
                prv = prv.prev


    @property
    def length(self):
        return self._length


    @length.setter
    def length(self, value):
        self._length = value

        this = self
        nxt = self.next

        while nxt != None:
            nxt.position = this.position + this.length
            this = nxt
            nxt = nxt.next

        self._updateArrays()


    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, value):
        self._position = value
        self._updateArrays()


    def _updateArrays(self):
        pts = max(2, int(STEPS_PER_NS * self.length / (self.speed * LIGHT_SPEED / NS_IN_S)))
        self.xs = np.linspace(self.position, self.position + self.length, pts, False)
        self.forward = np.zeros(pts)
        self.backward = np.zeros(pts)


    def reset(self):
        self._updateArrays()

