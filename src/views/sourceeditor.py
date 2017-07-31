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
from kivy.metrics import *
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from kivy.uix.boxlayout import BoxLayout

class SourceEditor(PopupEditor):
    """
    Supports wire editing.
    """

    impedanceTextField = ObjectProperty(None)
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

        self.animateSwitch(source.shape, False)

        self._anim = None

        self._setupIcons()


    def _setupIcons(self):
        """
        Add icons to buttons.
        """
        x = np.linspace(0, 10, 50)
        y = signal.gaussian(50, 7)
        self.gaussButton.container.add_widget(self._generateIcon(x, y))

        y0 = [0] * 10
        y = [1] * 30

        self.squareButton.container.add_widget(self._generateIcon(x, y0 + y + y0))

        y = []

        for i in range(15):
            y.append(i / 15.0)

        for i in range(15):
            y.append(1 - i / 15.0)

        self.triangleButton.container.add_widget(self._generateIcon(x, y0 + y + y0))


    def _generateIcon(self, x, y):
        fig, ax = plt.subplots()
        fig.set_tight_layout({"pad": 0})
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(axis = 'both', length = 0)
        ax.set_frame_on(False)
        ax.set_ylim([-0.1, 1.1])
        ax.plot(x, y, linewidth = dp(2), color = TEXT_BLACK)[0]
        return fig.canvas



    def on_focus(self, instance, focus):
        if instance == self.impedanceTextField.inputText and not focus:
            # Update impedance.
            if len(self.impedanceTextField.text) == 0:
                self._source.impedance = 0
            else:
                self._source.impedance = float(self.impedanceTextField.text)

        if instance == self.voltageTextField.inputText and not focus:
            # Update voltage.
            if len(self.voltageTextField.text) == 0:
                self._source.amplitude = 0
            else:
                self._source.amplitude = float(self.voltageTextField.text)

        if instance == self.widthTextField.inputText and not focus:
            # Update impedance.
            if len(self.widthTextField.text) == 0:
                self._source.width = 0
            else:
                self._source.width = float(self.widthTextField.text)


    def onWaveShapeClicked(self, shape):
        self._source.shape = shape
        self.animateSwitch(shape, True)


    def updateValues(self):
        self.prevButton.disabled = self._source.prev == None
        self.nextButton.disabled = self._source.next == None
        self.impedanceTextField.text = '{:g}'.format(self._source.impedance)
        self.impedanceTextField.inputText.input_filter = 'float'
        self.impedanceTextField.inputText.bind(focus = self.on_focus)
        self.voltageTextField.text = '{:g}'.format(self._source.amplitude)
        self.voltageTextField.inputText.input_filter = 'float'
        self.voltageTextField.inputText.bind(focus = self.on_focus)
        self.widthTextField.text = '{:g}'.format(self._source.width)
        self.widthTextField.inputText.input_filter = 'float'
        self.widthTextField.inputText.bind(focus = self.on_focus)
        self.impedanceTextField.animateLabel(False)
        self.voltageTextField.animateLabel(False)
        self.widthTextField.animateLabel(False)


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
