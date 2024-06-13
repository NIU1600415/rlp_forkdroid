from picamera2 import Picamera2
from lib.vision import Vision
from vision_processing.vision_processing import (
    analyze_frame_for_target_object,
    analyze_frame_for_destination,
)
from vision_processing.vision_processing import (
    TargetAnalysisResult,
    DestinationAnalysisResult,
)


class PhysVision(Vision):
    """Vision for the real robot (Pi camera)"""

    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()

    def get_frame(self):
        return self.picam2.capture_array()

    def detect_target(self) -> TargetAnalysisResult:
        frame = self.get_frame()
        analysis_result = analyze_frame_for_target_object(frame, debug=True)
        return analysis_result

    def detect_dest(self) -> DestinationAnalysisResult:
        frame = self.get_frame()
        analysis_result = analyze_frame_for_destination(frame, debug=True)
        return analysis_result
