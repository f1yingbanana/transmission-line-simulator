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

        self.positionTextField.text = '{:g}'.format(self._oscilloscope.position)
        self.positionTextField.inputText.input_filter = 'float'
        self.positionTextField.inputText.bind(focus = self.on_focus)
        self.positionTextField.animateLabel(False)

        if self._oscilloscope.maxTime <= 0:
            self.maxTimeTextField.text = ''
        else:
            self.maxTimeTextField.text = '{:g}'.format(self._oscilloscope.maxTime * 1e9)
        self.maxTimeTextField.inputText.input_filter = 'float'
        self.maxTimeTextField.inputText.bind(focus = self.on_focus)
        self.maxTimeTextField.animateLabel(False)


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()