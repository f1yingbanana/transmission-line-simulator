#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

"""
This is the number of discrete units of current we will measure. Bigger value
means smoother graphs.
"""
DISCRETE_STEPS = 200

PRIMARY = (21 / 255.0, 101 / 255.0, 192 / 255.0, 1)
LIGHT_PRIMARY = (94 / 255.0, 146 / 255.0, 243 / 255.0, 1)
DARK_PRIMARY = (0, 60 / 255.0, 143 / 255.0, 1)

TEXT_BLACK = (0, 0, 0, 0.86)
TEXT_GRAY = (0, 0, 0, 0.54)

WHITE = (1, 1, 1, 1)
DARK_GRAY = (224 / 255.0, 224 / 255.0, 224 / 255.0, 1)
GRAY = (245 / 255.0, 245 / 255.0, 245 / 255.0, 1)
LIGHT_GRAY = (250 / 255.0, 250 / 255.0, 250 / 255.0, 1)

RIPPLE_LIGHT = (1, 1, 1, 0.3)
RIPPLE_DARK = (0, 0, 0, 0.1)
RIPPLE_DURATION = 0.3

WIRE_THICKNESS = 8.0
WIRE_HIGHLIGHT = (0, 0, 0, 0.2)
