from lib.vision import Vision


class SimVision(Vision):
    """Vision for the real robot (Sim camera object)"""

    def __init__(self, sim):
        """TODO"""
        self.sim = sim

    def get_image(self, image):
        pass
