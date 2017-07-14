#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-3-2017
#

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
    resistance: the total resistance of the element, in ohms.
    """
    
    def __init__(self):
        self.position = 0
        self._length = 0
        self._next = None
        self._prev = None
        self.resistance = 0


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

