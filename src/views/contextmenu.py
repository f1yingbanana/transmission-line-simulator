#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-10-2017
#

from materialwidget import MaterialWidget
from materialbutton import MaterialButton
from kivy.properties import *
from kivy.lang.builder import Builder
from util.constants import *
from kivy.animation import Animation
from kivy.clock import Clock

class ContextMenu(MaterialWidget):
    """
    A contextual menu that displays text and icons.
    """

    _container = ObjectProperty(None)

    def __init__(self, titles, actions, icons = None, **kwargs):
        """
        Initializes this menu. Does not yet display it.

        titles:     list of strings for each item in the menu.
        actions:    list of callbacks that that takes no arguments.
        icons:      list of unicode strings for icons of each item. Default
                    None. Eg. [unichr(0xf26b)] 
        """
        super(ContextMenu, self).__init__(**kwargs)

        # Generate buttons according to title and icon
        for i in range(len(titles)):
            btn = MaterialButton()
            btn.changeStyle('flat')
            btn.title = titles[i]

            if icons != None:
                btn.icon = icons[i]
            else: 
                btn.icon = ''

            btn.onClick.append(actions[i])
            btn.onClick.append(lambda: self.dismiss(True))
            btn.size_hint_y = None
            btn.height = 60
            self._container.add_widget(btn)

        self._anim = None

        Clock.schedule_once(self._completeLayout, 0)


    def _completeLayout(self, dt):
        w = 0

        for child in self._container.children:
            w = max(w, child.width)

        for child in self._container.children:
            child.width = w



    def show(self, layer, pos, animated):
        # Determine orientation
        self.orientation = 'upright'

        h = len(self._container.children) * 60

        if pos[1] + h > layer.height:
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
                h = self._cachedPos[1] - self._container.minimum_height
                self._anim = Animation(size = self._container.minimum_size, y = h, opacity = 1.0, d = 0.2, t = 'in_out_quad')
            else:
                self._anim = Animation(size = self._container.minimum_size, opacity = 1.0, d = 0.2, t = 'in_out_quad')
            self._anim.start(self)
        else:
            self._anim = Animation(size = [0, 0], pos = self._cachedPos, d = 0.2, opacity = 0.0, t = 'in_out_quad')
            self._anim.start(self)


    def on_touch_down(self, touch):
        if not self.collide_point(touch.pos[0], touch.pos[1]):
            self.dismiss(True)

        return super(ContextMenu, self).on_touch_down(touch)
