#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-15-2017
#

from kivy.uix.togglebutton import ToggleButton

class MaterialRadioButton(ToggleButton):
    """
    Displays a radio button, which is grouped by group property.
    """
    def __init__(self, **kwargs):
        super(MaterialRadioButton, self).__init__(**kwargs)

        