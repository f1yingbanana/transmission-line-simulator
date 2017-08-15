#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-27-2017
#

from abstractcontroller import AbstractController
from views.simulatorview import SimulatorView
from models.model import Model
from models.model import AppState

class SimulatorController(AbstractController):
    """
    This is the root controller for the app. It manages the main areas of the
    app and updates everything else.
    """
    
    def __init__(self, parentWidget = None):
        super(SimulatorController, self).__init__(parentWidget)
        
        self.model = Model()
        self.view = SimulatorView()
        self.view.model = self.model

        if parentWidget != None:
            parentWidget.add_widget(self.view)

        self._elapsedTime = 0
        self._lastRedraw = 0
        self._lastRedrawTime = 0
        self._didRedraw = False

    
    def update(self, dt):
        super(SimulatorController, self).update(dt)
        
        if self.model.appState == AppState.Simulating:
            self.model.simulate(dt)
        
        self.view.update(dt)


    # Redrawing the matplotlib graphs are taking too long and should probably be 
    # separated in a different thread. But Matplotlib backend for kivy does not
    # support multithreading. So we just have to update graphs less often.
    # But how less often? We can profile how long it took to update the last
    # iteration, and adjust accordingly.
    def redrawGraph(self, dt):
        self._elapsedTime += dt

        if self._didRedraw:
            self._didRedraw = False
            self._lastRedrawTime = self._elapsedTime - self._lastRedraw

        if self._elapsedTime - self._lastRedraw > self._lastRedrawTime:
            self._lastRedraw = self._elapsedTime
            self.view.redrawGraph()
            self._didRedraw = True
            print self._lastRedrawTime
