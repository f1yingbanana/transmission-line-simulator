#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

import kivy
kivy.require('1.9.0')

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock
from controllers.simulatorcontroller import SimulatorController

def printme(dt):
    print "HW"



class SimulatorApp(App):
    """
    This is the root app for the simulator.
    """
    
    def build(self):
        """
        This returns a built widget for the app.
        """
        Config.set('graphics', 'window_state', 'maximized')
        
        # We should now load the root controller. The root controller should
        # handle the creation of UI. Then make the controller return the widget.
        self.rootController = SimulatorController()
        Clock.schedule_interval(self.rootController.update, 1.0 / 60.0)
        
        return self.rootController.view

# Entry point.
if __name__ == '__main__':
    SimulatorApp().run()
