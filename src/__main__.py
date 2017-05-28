#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.label import Label

class TransSim(App):
    """
    This is the root app for the simulator.
    """

    def build(self):
        """
        This returns a built widget for the app.
        """
        return Label(text='Hello world')

# Entry point.
if __name__ == '__main__':
    TransSim().run()
