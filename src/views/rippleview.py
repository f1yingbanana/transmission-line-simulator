#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-8-2017
#

from util.constants import *
from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.animation import Animation

class RippleView(Widget):
    """
    Displays a configurable ripple within the rectangular container.

    rippleColor:    the full color of the ripple.
    """

    rippleColor = ListProperty([])
    _currColor = ListProperty([])
    _rippleCenter = ListProperty([0, 0])
    _rippleRadius = NumericProperty(0.0)


    def __init__(self, **kwargs):
        super(RippleView, self).__init__(**kwargs)

        self._anim = None


    def ripple(self, center):
        """
        Starts a ripple animation centered at given location.
        """
        if self._anim != None:
            self._anim.cancel(self)

        self._rippleCenter = center
        self._rippleRadius = 1
        r = (self.width ** 2 + self.height ** 2) ** 0.5
        self._currColor = list(self.rippleColor)
        endColor = list(self.rippleColor)
        endColor[3] = 0
        self._anim = Animation(_rippleRadius = r, _currColor = endColor, d = RIPPLE_DURATION)
        self._anim.start(self)
