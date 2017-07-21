#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-17-2017
#

from kivy.properties import *
from popupeditor import PopupEditor
from util.constants import *


class OscilloscopeEditor(PopupEditor):
    """
    Draws the oscilloscope editor.
    """
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)

    minAmpTextField = ObjectProperty(None)
    maxWavesTextField = ObjectProperty(None)
    minWaveAmpTextField = ObjectProperty(None)
    maxTimeTextField = ObjectProperty(None)
    positionTextField = ObjectProperty(None)


    def __init__(self, oscilloscope, **kwargs):
        super(OscilloscopeEditor, self).__init__(**kwargs)

        self._oscilloscope = oscilloscope
        
        self.prevButton.changeStyle('flat')
        self.nextButton.changeStyle('flat')
        self.prevButton.iconLabel.color = PRIMARY
        self.nextButton.iconLabel.color = PRIMARY

        self.prevButton.on_press = self.showPrev
        self.nextButton.on_press = self.showNext


    def on_focus(self, instance, focus):
        if instance == self.minAmpTextField.inputText and not focus:
            if len(self.minAmpTextField.text) == 0:
                self._oscilloscope.minAmp = 0
            else:
                self._oscilloscope.minAmp = max(0, float(self.minAmpTextField.text))

        if instance == self.maxWavesTextField.inputText and not focus:
            if len(self.maxWavesTextField.text) == 0:
                self._oscilloscope.maxWaves = 0
            else:
                self._oscilloscope.maxWaves = max(0, int(self.maxWavesTextField.text))

        if instance == self.minWaveAmpTextField.inputText and not focus:
            if len(self.minWaveAmpTextField.text) == 0:
                self._oscilloscope.minWaveAmp = 0
            else:
                self._oscilloscope.minWaveAmp = max(0, float(self.minWaveAmpTextField.text))

        if instance == self.maxTimeTextField.inputText and not focus:
            if len(self.maxTimeTextField.text) == 0:
                self._oscilloscope.maxTime = 0
            else:
                self._oscilloscope.maxTime = max(0, float(self.maxTimeTextField.text) * 1e-9)

        if instance == self.positionTextField.inputText and not focus:
            if len(self.positionTextField.text) == 0:
                self._oscilloscope.position = 0
            else:
                self.reposition(self._oscilloscope, float(self.positionTextField.text))


    def updateValues(self):
        self.prevButton.disabled = self._oscilloscope.prev == None
        self.nextButton.disabled = self._oscilloscope.next == None

        if self._oscilloscope.minAmp == 0:
            self.minAmpTextField.text = ''
        else:
            self.minAmpTextField.text = '{:g}'.format(self._oscilloscope.minAmp)
        self.minAmpTextField.input_filter = 'float'
        self.minAmpTextField.inputText.bind(focus = self.on_focus)
        self.minAmpTextField.animateLabel(False)

        self.positionTextField.text = '{:g}'.format(self._oscilloscope.position)
        self.positionTextField.input_filter = 'float'
        self.positionTextField.inputText.bind(focus = self.on_focus)
        self.positionTextField.animateLabel(False)

        if self._oscilloscope.maxWaves == 0:
            self.maxWavesTextField.text = ''
        else:
            self.maxWavesTextField.text = '{:d}'.format(self._oscilloscope.maxWaves)
        self.maxWavesTextField.input_filter = 'int'
        self.maxWavesTextField.inputText.bind(focus = self.on_focus)
        self.maxWavesTextField.animateLabel(False)

        self.minWaveAmpTextField.text = '{:g}'.format(self._oscilloscope.minWaveAmp)
        self.minWaveAmpTextField.input_filter = 'float'
        self.minWaveAmpTextField.inputText.bind(focus = self.on_focus)
        self.minWaveAmpTextField.animateLabel(False)

        if self._oscilloscope.maxTime <= 0:
            self.maxTimeTextField.text = ''
        else:
            self.maxTimeTextField.text = '{:g}'.format(self._oscilloscope.maxTime * 1e9)
        self.maxTimeTextField.input_filter = 'float'
        self.maxTimeTextField.inputText.bind(focus = self.on_focus)
        self.maxTimeTextField.animateLabel(False)


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()