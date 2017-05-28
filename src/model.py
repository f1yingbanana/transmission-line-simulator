#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: May-28-2017
#

"""
This module contains the model classes for the transmission line simulation. 
"""


class Model(object):
    """
    An instance that keeps data on the simulation, including circuit info,
    wave generation, animations, and so on.
    """
    

class Circuit(object):
    """
    An instance that describes exactly how the circuit is set up. A circuit
    consists of a list of resistors connected in series or in parallel.
    """

class CircuitElement(object):
    """
    An abstract class that contains basic information on elements on a circuit.
    """

class Resistor(CircuitElement):
    """
    Represents a single resistor. A cable can also be thought as a resistor.
    """