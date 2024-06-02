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

    # def start(self):
    #     if not self.calibrated:
    #         print("Not calibrated; cannot start")
    #     print("Start looking for targets, moving them to destination")

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
        box_detected, box_position = self.vision.detect_box()
        if box_detected:
            self.motion.set_target_position(box_position)
            self.state = "Move to Box"
        else:
            self.state = "Detect Box"  # Continue detecting

    def move_to_box(self):
        print("Move to Box state")
        current_position = self.motion.get_current_position()
        if current_position is None or self.motion.target_position is None:
            return

        # Determine the direction to move
        if self.motion.is_arrived():
            self.state = "Lift Box"
        
        # Needs to be modified
        else:
            if current_position[0] < self.motion.target_position[0]:
                self.motion.move_forward()
                print("Move forward111")
            elif current_position[0] > self.motion.target_position[0]:
                self.motion.move_backward()
                print("Move backward")
            elif current_position[1] < self.motion.target_position[1]:
                self.motion.turn_left()
                print("Turn left")
            elif current_position[1] > self.motion.target_position[1]:
                self.motion.turn_right()
                print("Turn right")
            self.state = "Detect Box"
        

    def lift_box(self):
        print("Lift Box state")
        self.motion.lift_box()
        self.state = "Detect Dest"

    def detect_dest(self):
        print("Detect Dest state")
        dest_detected, dest_position = self.vision.detect_dest()
        if dest_detected:
            self.motion.set_target_position(dest_position)
            self.state = "Move to Dest"
        else:
            self.state = "Detect Dest"  # Continue detecting

    def move_to_dest(self):
        print("Move to Dest state")
        current_position = self.motion.get_current_position()
        if current_position is None or self.motion.target_position is None:
            return

        # Determine the direction to move
        if self.motion.is_arrived():
            self.state = "Leave Box"
        else:
            if current_position[0] < self.motion.target_position[0]:
                self.motion.move_forward()
            elif current_position[0] > self.motion.target_position[0]:
                self.motion.move_backward()
            elif current_position[1] < self.motion.target_position[1]:
                self.motion.move_left()
            elif current_position[1] > self.motion.target_position[1]:
                self.motion.move_right()
            self.state = "Detect Dest"

    def leave_box(self):
        print("Leave Box state")
        self.motion.leave_box()
        self.state = "IDLE"

    def stop(self):
        print("Stop state")
        self.motion.stop()

    def perform_state_actions(self):
        while True:
            if self.state == "IDLE":
                self.idle()
            elif self.state == "Detect Box":
                self.detect_box()
            elif self.state == "Move to Box":
                self.move_to_box()
            elif self.state == "Lift Box":
                self.lift_box()
            elif self.state == "Move to Dest":
                self.move_to_dest()
            elif self.state == "Leave Box":
                self.leave_box()
            elif self.state == "Detect Dest":
                self.detect_dest()
            elif self.state == "Stop":
                self.stop()
            time.sleep(0.1)


if __name__ == "__main__":
    print("Please use StateMachine class.")
