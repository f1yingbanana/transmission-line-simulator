#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jul-6-2017
#

from materialwidget import MaterialWidget
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior

class MaterialButton(MaterialWidget, ButtonBehavior):
    """
    This is a button in material widget style.
    """
    label = ObjectProperty(None)