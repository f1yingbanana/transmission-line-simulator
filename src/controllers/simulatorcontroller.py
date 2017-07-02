#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-27-2017
#

from abstractcontroller import AbstractController
from views.simulatorview import SimulatorView
from models.model import Model

class SimulatorController(AbstractController):
    """
    This is the root controller for the app. It manages the main areas of the
    app and updates everything else.
    """
    
    def __init__(self, parentWidget = None):
        super(SimulatorController, self).__init__(parentWidget)
        
        self.view = SimulatorView()
        self.model = Model()
    
    
    def update(self, dt):
        super(SimulatorController, self).update(dt)
        
        self.model.simulate(dt)
        self.view.update(dt)