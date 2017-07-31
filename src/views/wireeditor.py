#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-15-2017
#

from popupeditor import PopupEditor
from kivy.properties import *
from materialbutton import MaterialButton
from util.constants import *

class WireEditor(PopupEditor):
    """
    Supports wire editing.
    """

    impedanceTextField = ObjectProperty(None)
    lengthTextField = ObjectProperty(None)
    speedTextField = ObjectProperty(None)
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)

    def __init__(self, wire, **kwargs):
        super(WireEditor, self).__init__(**kwargs)

        self._wire = wire
        
        self.prevButton.changeStyle('flat')
        self.nextButton.changeStyle('flat')
        self.prevButton.iconLabel.color = PRIMARY
        self.nextButton.iconLabel.color = PRIMARY

        self.prevButton.on_press = self.showPrev
        self.nextButton.on_press = self.showNext


    def on_focus(self, instance, focus):
        if instance == self.impedanceTextField.inputText and not focus:
            # Update impedance.
            if len(self.impedanceTextField.text) == 0:
                self._wire.impedance = 0
            else:
                self._wire.impedance = float(self.impedanceTextField.text)

        if instance == self.lengthTextField.inputText and not focus:
            # Update position.
            if len(self.lengthTextField.text) == 0:
                self._wire.length = 0
            else:
                self._wire.length = max(0, float(self.lengthTextField.text))
                self.lengthTextField.text = '{:g}'.format(self._wire.length)

            self.updateCircuit()

        if instance == self.speedTextField.inputText and not focus:
            # Update speed.
            if len(self.speedTextField.text) == 0:
                self._wire.speed = 1
            else:
                self._wire.speed = min(1, max(0, float(self.speedTextField.text)))
                self.speedTextField.text = '{:g}'.format(self._wire.speed)

            self.updateCircuit()


    def updateValues(self):
        self.impedanceTextField.text = '{:g}'.format(self._wire.impedance)
        self.impedanceTextField.inputText.input_filter = 'float'
        self.impedanceTextField.inputText.bind(focus = self.on_focus)
        self.impedanceTextField.animateLabel(False)

        self.lengthTextField.text = '{:g}'.format(self._wire.length)
        self.lengthTextField.inputText.input_filter = 'float'
        self.lengthTextField.inputText.bind(focus = self.on_focus)
        self.lengthTextField.animateLabel(False)

        self.speedTextField.text = '{:g}'.format(self._wire.speed)
        self.speedTextField.inputText.input_filter = 'float'
        self.speedTextField.inputText.bind(focus = self.on_focus)
        self.speedTextField.animateLabel(False)

        self.prevButton.disabled = self._wire.prev == None
        self.nextButton.disabled = self._wire.next == None


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()
