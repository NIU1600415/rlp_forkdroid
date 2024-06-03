import time
from lib.motion import Motion
from lib.vision import Vision
from client_messaging.client_messaging import ClientMessaging, MessageFromClient, CalibrationData
from vision_processing.vision_processing import analyze_frame_for_target_object


class StateMachine:
    def __init__(self, client_messaging: ClientMessaging, motion: Motion, vision: Vision):
        self.client_messaging = client_messaging
        self.motion = motion
        self.vision = vision

        # State
        self.state = "IDLE"
        self.isArrived = 0
        self.calibrated: bool = False
        self.calibration_target: CalibrationData
        self.calibration_dest: CalibrationData

    def begin(self):
        while True:
            self.client_messaging.update()
            if self.client_messaging.message_ready():
                message = self.client_messaging.read_message()
                self.handle_message(message)
            self.perform_state_actions()
            time.sleep(1)

    def handle_message(self, message: MessageFromClient):
        print(f"STATEMACHINE received message: {message}")
        if message["type"] == "CALIBRATE_TARGET":
            self.calibrate_target()
        elif message["type"] == "CALIBRATE_DESTINATION":
            self.calibrate_destination()
        else:
            print("Unknown message type.")

    def calibrate_target(self):
        print("CALIBRATE TARGET")
        time.sleep(1)
        self.client_messaging.send({
            "type": "CALIB_DATA_TARGET",
            "data": {
                "upper": "#FEFEFE",
                "lower": "#FEFEFE"
            }
        })

    def calibrate_destination(self):
        print("CALIBRATE DEST")
        time.sleep(1)
        self.client_messaging.send({
            "type": "CALIB_DATA_DESTINATION",
            "data": {
                "upper": "#FEFEFE",
                "lower": "#FEFEFE"
            }
        })

    def idle(self):
        print("IDLE state")
        self.isArrived = 0
        self.state = "Detect Box"

    def detect_box(self):
        print("Detect Box state")
        box_detected, box_distance, box_angle = self.vision.detect_box()
        if box_detected:
            self.state = "Move to Box"
            self.move_to_box(box_distance, box_angle)
        else:
            self.state = "Detect Box"  # Continue detecting

    def move_to_box(self, distance, angle):
        print("Move to Box State")
        if angle < -10:
            self.motion.turn_left(duration=0.1)
            print("Turn left Box")
        elif angle > 10:
            self.motion.turn_right(duration=0.1)
            print("Turn right Box")
        elif distance > 0.1:
            self.motion.move_forward(duration=0.1)
            print("Move Forward Box")
        else:
            self.motion.stop()
            self.state = "Lift Box"

    def lift_box(self):
        print("Lift Box state")
        self.motion.lift_box()
        self.state = "Detect Dest"

    def detect_dest(self):
        print("Detect Dest state")
        dest_detected, dest_distance, dest_angle = self.vision.detect_dest()
        if dest_detected:
            self.state = 'Move to Dest'
            self.move_to_dest(dest_distance, dest_angle)
        else:
            self.state = "Detect Dest"

    def move_to_dest(self, distance, angle):
        print("Move to Dest state")
        if angle < -0.1:
            self.motion.turn_left(duration=0.1)
            print("Turn left Dest")
        elif angle > 0.1:
            self.motion.turn_right(duration=0.1)
            print("Turn right Dest")
        elif distance > 0.1:
            self.motion.move_forward(duration=0.1)
            print("Move forward Dest")
        else:
            self.motion.stop()
            self.state = "Leave Box"

    def leave_box(self):
        print("Leave Box state")
        self.motion.leave_box()
        self.state = "IDLE"

    def stop(self):
        print("Stop state")
        self.motion.stop()

    def perform_state_actions(self):
        if self.state == "IDLE":
            self.idle()
        elif self.state == "Detect Box":
            self.detect_box()
        elif self.state == "Move to Box":
            self.detect_box()  # Move to Box state calls detect_box to get distance and angle again
        elif self.state == "Lift Box":
            self.lift_box()
        elif self.state == "Move to Dest":
            self.detect_dest()  # Move to Dest state calls detect_dest to get distance and angle again
        elif self.state == "Leave Box":
            self.leave_box()
        elif self.state == "Detect Dest":
            self.detect_dest()
        elif self.state == "Stop":
            self.stop()
        time.sleep(0.1)


if __name__ == "__main__":
    print("Please use StateMachine class.")
