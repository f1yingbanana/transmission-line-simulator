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
    _slowDownButton = ObjectProperty(None)
    _speedUpButton = ObjectProperty(None)
    _speedLabel = ObjectProperty(None)
    _timeLabel = ObjectProperty(None)
    _statusLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PlaybackControlView, self).__init__(**kwargs)

        self.onReset = None


    def update(self, dt):
        if self.model != None:
            self._pauseButton.disabled = self.model.appState != AppState.Simulating
            self._speedLabel.text = str(int(self.model.simSpeed * 1e9)) + 'x'
            self._slowDownButton.disabled = self.model.simSpeed <= 1e-9
            self._speedUpButton.disabled = self.model.simSpeed >= 8e-9
            self._timeLabel.text = str(int(self.model.elapsed * 1e9)) + ' ns'
            self._statusLabel.text = 'Status: ' + self.model.appState


    def onPlayButtonClick(self):
        self.onReset()
        self.model.appState = AppState.Simulating


    def onPauseButtonClick(self):
        self.model.appState = AppState.Paused


    def onStopButtonClick(self):
        self.model.appState = AppState.Editing


    def onSlowDownButtonClick(self):
        if self.model.simSpeed > 1e-9:
            self.model.simSpeed /= 2


    def onSpeedUpButtonClick(self):
        if self.model.simSpeed < 8e-9:
            self.model.simSpeed *= 2
