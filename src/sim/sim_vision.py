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

    def detect_box(self):
        box_detected = True
        box_distance = 2.0
        box_angle = 5.0
        return box_detected, box_distance, box_angle

    def detect_dest(self):
        dest_detected = True
        dest_distance = 2.0
        dest_angle = -45.0
        return dest_detected, dest_distance, dest_angle

    def is_arrived(self):
        _, distance, _ = self.detect_dest()
        threshold = 0.1  # Example
        if abs(distance - threshold):
            return True
        return False
