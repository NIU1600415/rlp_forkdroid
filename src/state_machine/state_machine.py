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
        self.time_for_90_deg = 2
        self.velocity_for_time_calc = 4.2
        self.arrival_threshold_box = 2
        self.arrival_threshold_dest = 6
        self.forward_one_step_time = 1

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
        analysis_result = self.vision.detect_target()
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
            self.motion.turn_right(duration = 1)
            print("Rotating to scan for box")
            time.sleep(0.1)
            self.state = "DETECT_BOX"  # Continue detecting

    def move_to_box(self, distance, angle):
        print("MOVE_TO_BOX State")
        distance_vertical = distance * math.sin(math.radians(abs(angle)))
        if angle < -0.1:
            time_vertical_move = distance_vertical / self.velocity_for_time_calc
            self.motion.turn_left(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_vertical_move)
            self.motion.turn_right(duration=self.time_for_90_deg)
            print("Turn vertical_move Box")
        elif angle > 0.1:
            time_vertical_move = distance_vertical / self.velocity_for_time_calc
            self.motion.turn_right(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_vertical_move)
            self.motion.turn_left(duration=self.time_for_90_deg)
            print("Turn right Box")
        elif distance > self.arrival_threshold_box:
            # time_to_target = distance / self.velocity_for_time_calc
            # self.motion.move_forward(duration=time_to_target)
            self.motion.move_forward(duration = self.forward_one_step_time)
            print("Move Forward Box")
        elif distance < self.arrival_threshold_box:
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
            print(
                "DEST. DETECTED : ",
                analysis_result["destination_distance"],
                analysis_result["destination_frame_lateral_position_offset"]
            )
            self.state = "MOVE_TO_DEST"
            self.move_to_dest(
                analysis_result["destination_distance"], analysis_result["destination_frame_lateral_position_offset"]
            )  # Angle not provided
        else:
            self.motion.turn_right(duration = 1)
            print("Rotating to scan for dest.")
            time.sleep(0.1)
            self.state = "DETECT_DEST"

    def move_to_dest(self, distance, offset):
        frame_width = 1920
        pixel_offset = offset * (frame_width / 2)
        angle_per_pixel = 60 / frame_width
        angle = pixel_offset * angle_per_pixel
        distance_vertical = distance * math.sin(math.radians(abs(angle)))
        if offset < -0.2:
            time_vertical_move = distance_vertical / self.velocity_for_time_calc
            self.motion.turn_left(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_vertical_move)
            self.motion.turn_right(duration=self.time_for_90_deg)
            print("Turn left Dest")
        elif offset > 0.2:
            time_vertical_move = distance_vertical / self.velocity_for_time_calc
            self.motion.turn_right(duration=self.time_for_90_deg)
            self.motion.move_forward(duration=time_vertical_move)
            self.motion.turn_left(duration=self.time_for_90_deg)
            print("Turn right Dest")
        elif distance > self.arrival_threshold_dest:
            #time_to_dest = distance / selloc
            #self.motion.move_forward(duration=time_to_dest)
            self.motion.move_forward(duration=self.forward_one_step_time)
            print("Move Forward Dest")
        elif distance < self.arrival_threshold_dest:
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
