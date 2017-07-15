#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-14-2017
#

from popupeditor import PopupEditor
from kivy.properties import *
from materialbutton import MaterialButton
from util.constants import *
from kivy.animation import Animation
from models.powersource import *

class SourceEditor(PopupEditor):
    """
    Supports wire editing.
    """

    resistanceTextField = ObjectProperty(None)
    widthTextField = ObjectProperty(None)
    voltageTextField = ObjectProperty(None)
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)
    gaussButton = ObjectProperty(None)
    squareButton = ObjectProperty(None)
    triangleButton = ObjectProperty(None)
    triangleButton = ObjectProperty(None)
    selection = ObjectProperty(None)

    def __init__(self, source, **kwargs):
        super(SourceEditor, self).__init__(**kwargs)

        self._source = source
        self.resistanceTextField.text = '{:g}'.format(source.resistance)
        self.resistanceTextField.input_filter = 'float'
        self.resistanceTextField.inputText.bind(focus = self.on_focus)
        self.voltageTextField.text = '{:g}'.format(source.amplitude)
        self.voltageTextField.input_filter = 'float'
        self.voltageTextField.inputText.bind(focus = self.on_focus)
        self.widthTextField.text = '{:g}'.format(source.width)
        self.widthTextField.input_filter = 'float'
        self.widthTextField.inputText.bind(focus = self.on_focus)

        self.gaussButton.changeStyle('flat')
        self.squareButton.changeStyle('flat')
        self.triangleButton.changeStyle('flat')
        self.prevButton.changeStyle('flat')
        self.nextButton.changeStyle('flat')
        self.prevButton.iconLabel.color = PRIMARY
        self.nextButton.iconLabel.color = PRIMARY

        self.prevButton.on_press = self.showPrev
        self.nextButton.on_press = self.showNext
        self.gaussButton.on_press = lambda: self.onWaveShapeClicked(WaveShape.Gaussian)
        self.squareButton.on_press = lambda: self.onWaveShapeClicked(WaveShape.Square)
        self.triangleButton.on_press = lambda: self.onWaveShapeClicked(WaveShape.Triangle)

        self.prevButton.disabled = source.prev == None
        self.nextButton.disabled = source.next == None

        self.animateSwitch(source.shape, False)

        self._anim = None


    def on_focus(self, instance, focus):
        if instance == self.resistanceTextField.inputText and not focus:
            # Update resistance.
            if len(self.resistanceTextField.text) == 0:
                self._source.resistance = 0
            else:
                self._source.resistance = float(self.resistanceTextField.text)

        if instance == self.voltageTextField.inputText and not focus:
            # Update voltage.
            if len(self.voltageTextField.text) == 0:
                self._source.amplitude = 0
            else:
                self._source.amplitude = float(self.voltageTextField.text)

        if instance == self.widthTextField.inputText and not focus:
            # Update resistance.
            if len(self.widthTextField.text) == 0:
                self._source.width = 0
            else:
                self._source.width = float(self.widthTextField.text)


    def onWaveShapeClicked(self, shape):
        self._source.shape = shape
        self.animateSwitch(shape, True)


    def animateSwitch(self, mode, animated):
        if self._anim != None:
            self._anim.cancel(self.selection)

        t = 0.3 if animated else 0

        if mode == WaveShape.Gaussian:
            self._anim = Animation(center = self.gaussButton.center, d = t, t = 'in_out_quad')
        elif mode == WaveShape.Square:
            self._anim = Animation(center = self.squareButton.center, d = t, t = 'in_out_quad')
        else:
            self._anim = Animation(center = self.triangleButton.center, d = t, t = 'in_out_quad')

        self._anim.start(self.selection)


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()
