#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-6-2017
#

from materialwidget import MaterialWidget
from kivy.properties import *
from kivy.uix.behaviors import ButtonBehavior
from util.hoverbehavior import HoverBehavior
from kivy.animation import Animation


class MaterialButton(MaterialWidget, ButtonBehavior, HoverBehavior):
    """
    This is a button in material widget style.
    """
    titleLabel = ObjectProperty(None)

    iconLabel = ObjectProperty(None)

    _currHighlightColor = ListProperty([0, 0, 0, 0])

    highlightColor = ListProperty(None)

    def __init__(self, **kwargs):
        super(MaterialButton, self).__init__(**kwargs)

        self.onClick = []
        self.hovering = False
        self._hoverAnim = None


    def on_enter(self):
        self.hovering = True

        if self._hoverAnim != None:
            self._hoverAnim.cancel(self)

        self._hoverAnim = Animation(elevation = 8, d = 0.2, t = 'in_out_cubic')
        self._hoverAnim.start(self)


    def on_leave(self):
        self.hovering = False

        if self._hoverAnim != None:
            self._hoverAnim.cancel(self)

        self._hoverAnim = Animation(elevation = 2, d = 0.2, t = 'in_out_cubic')
        self._hoverAnim.start(self)


    def on_press(self):
        # Dispatch ink ripple
        pass


    def on_release(self):
        for e in self.onClick:
            e()