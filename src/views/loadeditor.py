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

    impedanceTextField = ObjectProperty(None)
    prevButton = ObjectProperty(None)
    nextButton = ObjectProperty(None)

    def __init__(self, load, **kwargs):
        super(LoadEditor, self).__init__(**kwargs)

        self._load = load
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
                self._load.impedance = 0
            else:
                self._load.impedance = float(self.impedanceTextField.text)


    def updateValues(self):
        self.prevButton.disabled = self._load.prev == None
        self.nextButton.disabled = self._load.next == None
        self.impedanceTextField.text = '{:g}'.format(self._load.impedance)
        self.impedanceTextField.inputText.input_filter = 'float'
        self.impedanceTextField.inputText.bind(focus = self.on_focus)
        self.impedanceTextField.animateLabel(False)


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()
