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
        self.state = "INIT"
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

    def start(self):
        if not self.calibrated:
            print("Not calibrated; cannot start")
        print("Start looking for targets, moving them to destination")

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

    def perform_state_actions(self):
        pass
        # print(f"Current state: {self.state}")


if __name__ == "__main__":
    print("Please use StateMachine class.")
