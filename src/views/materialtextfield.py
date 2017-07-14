#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-12-2017
#

from kivy.properties import *
from kivy.metrics import *
from kivy.uix.textinput import TextInput
from kivy.uix.relativelayout import RelativeLayout
from util.hoverbehavior import HoverBehavior
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.widget import Widget

class MaterialTextField(HoverBehavior, RelativeLayout):
    """
    Implements the material standard text input (partially) that is enough for
    this project.
    """

    label = ObjectProperty(None)
    inputText = ObjectProperty(None)
    bottomLine = ObjectProperty(None)
    prefix = ObjectProperty(None)
    suffix = ObjectProperty(None)

    primaryColor = ListProperty()
    errorColor = ListProperty()
    unfocusedLabelColor = ListProperty()
    disabledLabelColor = ListProperty()
    unfocusedLineColor = ListProperty()
    focusedLineColor = ListProperty()
    textColor = ListProperty()

    def __init__(self, **kwargs):
        super(MaterialTextField, self).__init__(**kwargs)

        self._labelAnim = None
        self._bottomLineAnim = None
        self._suffixAnim = None
        self._prefixAnim = None

        Clock.schedule_once(self._completeSetup, 0)


    def _completeSetup(self, dt):
        self.inputText.bind(focus = self.on_focus)


    def on_focus(self, instance, focus):
        t = focus or (instance.text != None and len(instance.text) > 0)
        self._animateLabel(t)


    def _animateLabel(self, shrink):
        if self._labelAnim != None:
            self._labelAnim.cancel(self.label)
            self._bottomLineAnim.cancel(self.bottomLine)
            self._prefixAnim.cancel(self.prefix)
            self._suffixAnim.cancel(self.suffix)

        y0 = dp(8)
        y1 = self.inputText.y + self.inputText.line_height + dp(8)

        f0 = sp(16)
        f1 = sp(12)

        c0 = self.unfocusedLineColor
        c1 = self.primaryColor

        h0 = dp(1)
        h1 = dp(2)

        lc0 = self.unfocusedLabelColor
        lc1 = self.primaryColor

        if shrink:
            self._labelAnim = Animation(y = y1, font_size = f1, d = 0.15, t = 'in_out_quad')
            self._prefixAnim = Animation(opacity = 1, d = 0.15, t = 'in_out_quad')
            self._suffixAnim = Animation(opacity = 1, d = 0.15, t = 'in_out_quad')
        else:
            self._labelAnim = Animation(y = y0, color = lc0, font_size = f0, d = 0.15, t = 'in_out_quad')
            self._prefixAnim = Animation(opacity = 0, d = 0.15, t = 'in_out_quad')
            self._suffixAnim = Animation(opacity = 0, d = 0.15, t = 'in_out_quad')

        if self.inputText.focus:
            self._labelAnim &= Animation(color = lc1, d = 0.15, t = 'in_out_quad')
            self._bottomLineAnim = Animation(color = c1, height = h1, d = 0.15, t = 'in_out_quad')
        else:
            self._labelAnim &= Animation(color = lc0, d = 0.15, t = 'in_out_quad')
            self._bottomLineAnim = Animation(color = c0, height = h0, d = 0.15, t = 'in_out_quad')

        self._suffixAnim.start(self.suffix)
        self._prefixAnim.start(self.prefix)
        self._labelAnim.start(self.label)
        self._bottomLineAnim.start(self.bottomLine)


    def on_enter(self):
        if not self.inputText.focus:
            if self._bottomLineAnim != None:
                self._bottomLineAnim.cancel(self.bottomLine)

            self._bottomLineAnim = Animation(color = self.focusedLineColor, height = dp(2), d = 0.15, t = 'in_out_quad')
            self._bottomLineAnim.start(self.bottomLine)


    def on_leave(self):
        if not self.inputText.focus:
            if self._bottomLineAnim != None:
                self._bottomLineAnim.cancel(self.bottomLine)

            self._bottomLineAnim = Animation(color = self.unfocusedLineColor, height = dp(1), d = 0.15, t = 'in_out_quad')
            self._bottomLineAnim.start(self.bottomLine)



class Underline(Widget):
    """
    Helper view for the underline of the text field.
    """
    thickness = NumericProperty(None)

