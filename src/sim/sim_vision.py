from numpy import frombuffer, flipud, uint8
from lib.vision import Vision
from vision_processing.vision_processing import (
    analyze_frame_for_target_object,
    analyze_frame_for_destination,
)
from vision_processing.vision_processing import (
    TargetAnalysisResult,
    DestinationAnalysisResult,
)


class SimVision(Vision):
    """Vision for the real robot (Sim camera object)"""

    def __init__(self, sim):
        self.sim = sim
        self.camera_handle = sim.getObject("/RobotnikSummitXL/Vision_sensor")

    def get_frame(self):
        image, resolution = self.sim.getVisionSensorImg(self.camera_handle)
        frame = frombuffer(image, dtype=uint8)
        frame.resize([resolution[1], resolution[0], 3])
        # vision sensor image is vertically flipped, correct it.
        frame = flipud(frame)
        return frame

    def detect_target(self) -> TargetAnalysisResult:
        frame = self.get_frame()
        analysis_result = analyze_frame_for_target_object(frame, debug=True)
        return analysis_result

    def detect_dest(self) -> DestinationAnalysisResult:
        frame = self.get_frame()
        analysis_result = analyze_frame_for_destination(frame, debug=True)
        return analysis_result

    def has_arrived(self):
        analysis_result = self.detect_dest()
        threshold = 0.1  # Example
        return analysis_result["destination_distance"] < threshold
