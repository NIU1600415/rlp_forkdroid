import time, math
from lib.motion import Motion
from lib.vision import Vision
from client_messaging.client_messaging import (
    ClientMessaging,
    MessageFromClient,
    CalibrationData,
)


class StateMachine:
    def __init__(
        self, client_messaging: ClientMessaging, motion: Motion, vision: Vision
    ):
        self.client_messaging = client_messaging
        self.motion = motion
        self.vision = vision

        # State
        self.state = "IDLE"
        self.is_arrived = 0
        self.calibrated: bool = False
        self.calibration_target: CalibrationData
        self.calibration_dest: CalibrationData
        self.time_for_90_deg = 1.4
        self.time_for_velocity_calc = 8

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
        self.client_messaging.send(
            {
                "type": "CALIB_DATA_TARGET",
                "data": {"upper": "#FEFEFE", "lower": "#FEFEFE"},
            }
        )

    def calibrate_destination(self):
        print("CALIBRATE DEST")
        time.sleep(1)
        self.client_messaging.send(
            {
                "type": "CALIB_DATA_DESTINATION",
                "data": {"upper": "#FEFEFE", "lower": "#FEFEFE"},
            }
        )

    def idle(self):
        print("IDLE state")
        self.is_arrived = 0
        self.state = "DETECT_BOX"

    def detect_box(self):
        print("DETECT_BOX state")
        analysis_result = self.vision.detect_box()
        if analysis_result["target_detected"]:
            print(
                "BOX DETECTED : ",
                analysis_result["target_distance"],
                analysis_result["target_rotation"],
            )
            self.state = "MOVE_TO_BOX"
            self.move_to_box(
                analysis_result["target_distance"], analysis_result["target_rotation"]
            )
        else:
            print("BOX NOT DETECTED YET")
            self.state = "DETECT_BOX"  # Continue detecting

    def move_to_box(self, distance, angle):
        print("MOVE_TO_BOX State")
        if angle < 0:
            distance_vertical = distance * math.sin(math.radians(abs(angle)))
            time_left = distance_vertical / self.time_for_velocity_calc
            self.motion.turn_left(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_left)
            self.motion.turn_right(duration=self.time_for_90_deg)
            print("Turn left Box")
        elif angle > 0:
            distance_vertical = distance * math.sin(math.radians(abs(angle)))
            time_left = distance_vertical / self.time_for_velocity_calc
            self.motion.turn_right(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_left)
            self.motion.turn_left(duration=self.time_for_90_deg)
            print("Turn right Box")
        elif distance > 5:
            self.motion.move_forward(duration=0.5)
            print("Move Forward Box")
        else:
            self.motion.stop()
            self.state = "LIFT_BOX"

    def lift_box(self):
        print("LIFT_BOX state")
        self.motion.lift_target()
        self.state = "DETECT_DEST"

    def detect_dest(self):
        print("DETECT_DEST state")
        analysis_result = self.vision.detect_dest()
        if analysis_result["destination_detected"]:
            self.state = "MOVE_TO_DEST"
            self.move_to_dest(
                analysis_result["destination_distance"], 0
            )  # Angle not provided
        else:
            self.state = "DETECT_DEST"

    def move_to_dest(self, distance, angle):
        print("MOVE_TO_DEST state")
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
            self.state = "LEAVE_BOX"

    def leave_box(self):
        print("LEAVE_BOX state")
        self.motion.place_target()
        self.state = "IDLE"

    def stop(self):
        print("STOP state")
        self.motion.stop()

    def perform_state_actions(self):
        if self.state == "IDLE":
            self.idle()
        elif self.state == "DETECT_BOX":
            self.detect_box()
        elif self.state == "MOVE_TO_BOX":
            self.detect_box()  # MOVE_TO_BOX state calls detect_box to get distance and angle again
        elif self.state == "LIFT_BOX":
            self.lift_box()
        elif self.state == "MOVE_TO_DEST":
            self.detect_dest()  # MOVE_TO_DEST state calls detect_dest to get distance and angle again
        elif self.state == "LEAVE_BOX":
            self.leave_box()
        elif self.state == "DETECT_DEST":
            self.detect_dest()
        elif self.state == "STOP":
            self.stop()
        time.sleep(0.1)


if __name__ == "__main__":
    print("Please use StateMachine class.")
