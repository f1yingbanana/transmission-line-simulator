#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-24-2017
#

from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.animation import Animation

class ExportDialog(Widget):
    """
    Brings up an export dialog that covers the whole screen, asking for a name
    to export the two files to.
    """

    titleLabel = ObjectProperty(None)
    subtitleLabel = ObjectProperty(None)
    textField = ObjectProperty(None)
    _box = ObjectProperty(None)
    _bg = ObjectProperty(None)
    _cancelButton = ObjectProperty(None)
    _confirmButton = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ExportDialog, self).__init__(**kwargs)
        self._bgAnim = None
        self._boxAnim = None
        self._cancelButton.changeStyle('flat')
        self._confirmButton.changeStyle('flat')
        self._cancelButton.onClick.append(self._onCancelClicked)
        self._confirmButton.onClick.append(self._onConfirmClicked)
        self.onConfirmClicked = []
    

    def show(self, layer):
        layer.add_widget(self)
        self._animate(True)


    def dismiss(self, animated):
        if not animated:
            self.parent.remove_widget(self)
        else:
            self._animate(False)
            self._bgAnim.on_complete = self._animComplete


    def _animComplete(self, x):
        if self.parent != None:
            self.parent.remove_widget(self)


    def _animate(self, isEntering):
        if self._bgAnim != None:
            self._bgAnim.cancel(self)
            self._boxAnim.cancel(self)

        if isEntering:
            self._bgAnim = Animation(opacity = 1.0, d = 0.35, t = 'in_out_quad')
            self._bgAnim.start(self._bg)
            self._boxAnim = Animation(center_y = self.center_y, d = 0.35, t = 'in_out_quad')
            self._boxAnim.start(self._box)
        else:
            self._bgAnim = Animation(opacity = 0, d = 0.35, t = 'in_out_quad')
            self._bgAnim.start(self._bg)
            self._boxAnim = Animation(center_y = -self._box.height, d = 0.35, t = 'in_out_quad')
            self._boxAnim.start(self._box)


    def _onConfirmClicked(self):
        self.dismiss(True)
        
        for e in self.onConfirmClicked:
            e(self.textField.text)


    def _onCancelClicked(self):
        self.dismiss(True)


    def on_touch_down(self, touch):
        if not self._box.collide_point(touch.pos[0], touch.pos[1]):
            self.dismiss(True)

        for c in self.children:
            if c.on_touch_down(touch):
                return True

        return True

