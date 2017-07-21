#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-21-2017
#

from materialwidget import MaterialWidget

class OscilloscopeGraphView(MaterialWidget):
    """
    This manages the display of a specific oscilloscope, with functions to zoom,
    pan, export, and value display.
    """
    def __init__(self, oscilloscope, **kwargs):
        super(OscilloscopeGraphView, self).__init__(**kwargs)

        self.oscilloscope = oscilloscope

    