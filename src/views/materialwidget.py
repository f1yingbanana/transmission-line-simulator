#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-28-2017
#

from kivy.uix.widget import Widget
from kivy.properties import *
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import *
from PIL import Image, ImageDraw, ImageFilter

class MaterialWidget(Widget):
    """
    The basic UI element layout, automatically draws and updates its shadows.

    raised: whether this widget has an edge and shadow.
    """
    
    keyShadowTexture = ObjectProperty(None)
    
    ambientShadowTexture = ObjectProperty(None)
    
    raised = BooleanProperty(True)

    clipSubviews = BooleanProperty(False)

    elevation = NumericProperty(2.0)

    backgroundColor = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        super(MaterialWidget, self).__init__(**kwargs)
        
    
    def on_size(self, *args, **kwargs):
        self._updateShadow()


    def on_pos(self, *args, **kwargs):
        self._updateShadow()


    def on_elevation(self, *args, **kwargs):
        self._updateShadow()


    def _updateShadow(self):
        # Shadow 1
        offset_y = self.elevation
        radius = self.elevation / 2.0
        t1 = self._genShadow(self.size[0], self.size[1], radius, 0.26)
        self.keyShadowTexture = t1

        # Shadow 2
        radius = self.elevation
        t2 = self._genShadow(self.size[0], self.size[1], radius, 0.05)
        self.ambientShadowTexture = t2


    def _genShadow(self, ow, oh, radius, alpha):
        # We need a bigger texture to correctly blur the edges
        w = ow + radius * 6.0
        h = oh + radius * 6.0
        w = int(w)
        h = int(h)
        texture = Texture.create(size=(w, h), colorfmt='rgba')
        im = Image.new('RGBA', (w, h), color=(1, 1, 1, 0))

        draw = ImageDraw.Draw(im)
        # the rectangle to be rendered needs to be centered on the texture
        x0, y0 = (w - ow) / 2., (h - oh) / 2.
        x1, y1 = x0 + ow - 1, y0 + oh - 1
        draw.rectangle((x0, y0, x1, y1), fill=(0, 0, 0, int(255 * alpha)))
        im = im.filter(ImageFilter.GaussianBlur(radius))
        texture.blit_buffer(im.tobytes(), colorfmt='rgba', bufferfmt='ubyte')

        return texture

