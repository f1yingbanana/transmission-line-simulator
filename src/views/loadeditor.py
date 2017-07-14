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

class LoadEditor(PopupEditor):
    """
    Supports wire editing.
    """

    resistanceTextField = ObjectProperty(None)
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)

    def __init__(self, load, **kwargs):
        super(LoadEditor, self).__init__(**kwargs)

        self.resistanceTextField.text = '{:g}'.format(load.resistance)
        self.resistanceTextField.input_filter = 'float'
        self._load = load
        self.resistanceTextField.inputText.bind(focus = self.on_focus)
        self.prevButton.changeStyle('flat')
        self.nextButton.changeStyle('flat')
        self.prevButton.iconLabel.color = PRIMARY
        self.nextButton.iconLabel.color = PRIMARY

        self.prevButton.disabled = load.prev == None
        self.nextButton.disabled = load.next == None


    def on_focus(self, instance, focus):
        if instance == self.resistanceTextField.inputText and not focus:
            # Update resistance.
            if len(self.resistanceTextField.text) == 0:
                self._load.resistance = 0
            else:
                self._load.resistance = float(self.resistanceTextField.text)