from numpy import frombuffer, flipud, uint8
from lib.vision import Vision


class SimVision(Vision):
    """Vision for the real robot (Sim camera object)"""

    def __init__(self, sim):
        self.sim = sim
        self.camera_handle = sim.getObject("/Vision_sensor")

    def get_frame(self):
        image, resolution = self.sim.getVisionSensorImg(self.camera_handle)
        frame = frombuffer(image, dtype=uint8)
        frame.resize([resolution[1], resolution[0], 3])
        # vision sensor image is vertically flipped, correct it.
        frame = flipud(frame)
        return frame
