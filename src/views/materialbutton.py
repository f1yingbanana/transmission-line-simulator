#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-6-2017
#

from materialwidget import MaterialWidget
from rippleview import RippleView
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from util.hoverbehavior import HoverBehavior
from kivy.animation import Animation


class MaterialButton(ButtonBehavior, MaterialWidget, HoverBehavior):
    """
    This is a button in material widget style.
    """

    _rippleView = ObjectProperty(None)

    titleLabel = ObjectProperty(None)

    iconLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MaterialButton, self).__init__(**kwargs)

        self.onClick = []
        self.hovering = False
        self._hoverAnim = None


    def on_enter(self):
        if self.disabled:
            return

        self.hovering = True
        self._animateHover()


    def on_disabled(self, instance, value):
        super(MaterialButton, self).on_disabled(instance, value)

        self.hovering = False
        self._animateHover()

    def on_leave(self):
        if self.disabled:
            return

        self.hovering = False
        self._animateHover()


    def _animateHover(self):
        if self._hoverAnim != None:
            self._hoverAnim.cancel(self)

        e = 8 if self.hovering else 2
        self._hoverAnim = Animation(elevation = e, d = 0.2, t = 'in_out_cubic')
        self._hoverAnim.start(self)



    def on_press(self):
        if self.disabled:
            return

        self._rippleView.ripple(self.last_touch.pos)


    def on_release(self):
        if self.disabled:
            return
        
        for e in self.onClick:
            e()
