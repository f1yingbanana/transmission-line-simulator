#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-14-2017
#

from materialwidget import MaterialWidget
from materialbutton import MaterialButton
from kivy.properties import *
from kivy.lang.builder import Builder
from util.constants import *
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import *

class PopupEditor(MaterialWidget):
    """
    An abstract pop up that allows widget editing. This factors out presentation
    but actual editing values should be extended by subclassing.
    """

    _container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PopupEditor, self).__init__(**kwargs)

        self._anim = None
        self.elevation = dp(8)

        Clock.schedule_once(self._completeLayout, 0)


    def _completeLayout(self, dt):
        pass



    def show(self, layer, pos, animated):
        # Determine orientation
        self.orientation = 'upright'

        if pos[1] + self._fullSize[1] > layer.height:
            self.orientation = 'downright'

        layer.add_widget(self)

        self.pos = pos
        self._cachedPos = pos

        if animated:
            self.size = 0, 0
            self.opacity = 0.0

            self._animate(True)
        else:
            self.size = self._container.minimum_size
            self.opacity = 1.0

            if self.orientation == 'downright':
                self.y = pos[1] - h


    def dismiss(self, animated):
        if not animated:
            self.parent.remove_widget(self)
            self.size = 0, 0
            self.opacity = 0.0
        else:
            self._animate(False)
            self._anim.on_complete = lambda x: self.parent.remove_widget(self)


    def _animate(self, isEntering):
        if self._anim != None:
            self._anim.cancel(self)

        if isEntering:
            if self.orientation == 'downright':
                h = self._cachedPos[1] - self._fullSize[1]
                self._anim = Animation(size = self._fullSize, y = h, opacity = 1.0, d = 0.2, t = 'in_out_quad')
            else:
                self._anim = Animation(size = self._fullSize, opacity = 1.0, d = 0.2, t = 'in_out_quad')
            self._anim.start(self)
        else:
            self._anim = Animation(size = [0, 0], pos = self._cachedPos, d = 0.2, opacity = 0.0, t = 'in_out_quad')
            self._anim.start(self)


    def on_touch_down(self, touch):
        if not self.collide_point(touch.pos[0], touch.pos[1]):
            self.dismiss(True)

        return super(PopupEditor, self).on_touch_down(touch)
