#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-8-2017
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from models.model import *

class PlaybackControlView(BoxLayout):
    """
    Displays playback control elements of the simulation, including play, pause
    and stop buttons.
    """

    _playButton = ObjectProperty(None)
    _pauseButton = ObjectProperty(None)
    _stopButton = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlaybackControlView, self).__init__(**kwargs)


    def update(self, dt):
        if self.model != None:
            self._pauseButton.disabled = self.model.appState != AppState.Simulating


    def onPlayButtonClick(self):
        self.model.appState = AppState.Simulating


    def onPauseButtonClick(self):
        self.model.appState = AppState.Paused


    def onStopButtonClick(self):
        self.model.reset()
        self.model.appState = AppState.Editing
