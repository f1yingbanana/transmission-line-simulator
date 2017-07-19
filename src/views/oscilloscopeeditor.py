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
        '''
        if instance == self.resistanceTextField.inputText and not focus:
            # Update resistance.
            if len(self.resistanceTextField.text) == 0:
                self._load.resistance = 0
            else:
                self._load.resistance = float(self.resistanceTextField.text)
                '''


    def updateValues(self):
        self.prevButton.disabled = self._load.prev == None
        self.nextButton.disabled = self._load.next == None

        '''
        self.resistanceTextField.text = '{:g}'.format(self._load.resistance)
        self.resistanceTextField.input_filter = 'float'
        self.resistanceTextField.inputText.bind(focus = self.on_focus)
        self.resistanceTextField.animateLabel(False)
        '''


    def showPrev(self):
        self.onPrev()


    def showNext(self):
        self.onNext()