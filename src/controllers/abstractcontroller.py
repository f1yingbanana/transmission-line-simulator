#
# Transmission Line Simulator
# 
# Author(s): Jiacong Xu
# Created: Jun-27-2017
#

class AbstractController(object):
    """
    A template for controllers in the app. Each controller can manage a view and
    is updated regularly.
    
    Properties
    view:   The view this controller is managing. Can be None.
    """
    
    def update(self, dt):
        """
        The main update function. This is called every frame at 60 fps.
        """
        pass
    
    def __init__(self, parentWidget = None):
        """
        Initializes this controller with the parentWidget being the container
        for the view, if any.
        """
        self.view = None
        