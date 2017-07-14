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

    resistanceTextField = ObjectProperty(None)
    lengthTextField = ObjectProperty(None)
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)

    def __init__(self, wire, **kwargs):
        super(WireEditor, self).__init__(**kwargs)

        self._wire = wire
        
        self.resistanceTextField.text = '{:g}'.format(wire.resistance)
        self.resistanceTextField.input_filter = 'float'
        self.resistanceTextField.inputText.bind(focus = self.on_focus)

        self.lengthTextField.text = '{:g}'.format(wire.length)
        self.lengthTextField.input_filter = 'float'
        self.lengthTextField.inputText.bind(focus = self.on_focus)

        self.prevButton.changeStyle('flat')
        self.nextButton.changeStyle('flat')
        self.prevButton.iconLabel.color = PRIMARY
        self.nextButton.iconLabel.color = PRIMARY

        self.prevButton.disabled = wire.prev == None
        self.nextButton.disabled = wire.next == None


    def on_focus(self, instance, focus):
        if instance == self.resistanceTextField.inputText and not focus:
            # Update resistance.
            if len(self.resistanceTextField.text) == 0:
                self._wire.resistance = 0
            else:
                self._wire.resistance = float(self.resistanceTextField.text)

        if instance == self.lengthTextField.inputText and not focus:
            # Update position.
            if len(self.lengthTextField.text) == 0:
                self._wire.length = 0
            else:
                self._wire.length = max(0, float(self.lengthTextField.text))
                self.lengthTextField.text = '{:g}'.format(self._wire.length)

            self.update()