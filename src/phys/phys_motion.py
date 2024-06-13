import time
import Adafruit_PCA9685
from lib.motion import Motion

DIRECTIONS = {
    "FR": {
        "STOP": 260,
        "FORWARD": 208,
        "BACKWARD": 322,
    },
    "FL": {
        "STOP": 403,
        "FORWARD": 500,
        "BACKWARD": 300,
    },
    "BL": {
        "STOP": 400,
        "FORWARD": 413,
        "BACKWARD": 390,
    },
    "BR": {
        "STOP": 410,
        "FORWARD": 465,
        "BACKWARD": 350,
    },
}
FORKS_DOWN = 580
FORKS_UP = 150


class PhysMotion(Motion):
    """Motion for the real robot."""

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.fr_servo_index = 1
        self.fl_servo_index = 2
        self.bl_servo_index = 4
        self.br_servo_index = 5
        self.fork_servo_index = 0

    def _set_fr(self, angle):
        self.pwm.set_pwm(self.fr_servo_index, 0, angle)

    def _set_fl(self, angle):
        self.pwm.set_pwm(self.fl_servo_index, 0, angle)

    def _set_bl(self, angle):
        self.pwm.set_pwm(self.bl_servo_index, 0, angle)

    def _set_br(self, angle):
        self.pwm.set_pwm(self.br_servo_index, 0, angle)

    def _set_forks(self, angle):
        self.pwm.set_pwm(self.fork_servo_index, 0, angle)

    def move_forward(self, duration):
        self._set_fr(DIRECTIONS["FR"]["FORWARD"])
        self._set_fl(DIRECTIONS["FL"]["FORWARD"])
        self._set_bl(DIRECTIONS["BL"]["FORWARD"])
        self._set_br(DIRECTIONS["BR"]["FORWARD"])
        time.sleep(duration)

    def move_backward(self, duration):
        self._set_fr(DIRECTIONS["FR"]["BACKWARD"])
        self._set_fl(DIRECTIONS["FL"]["BACKWARD"])
        self._set_bl(DIRECTIONS["BL"]["BACKWARD"])
        self._set_br(DIRECTIONS["BR"]["BACKWARD"])
        time.sleep(duration)

    def turn_left(self, duration):
        self._set_fr(DIRECTIONS["FR"]["FORWARD"])
        self._set_fl(DIRECTIONS["FL"]["BACKWARD"])
        self._set_bl(DIRECTIONS["BL"]["BACKWARD"])
        self._set_br(DIRECTIONS["BR"]["FORWARD"])
        time.sleep(duration)

    def turn_right(self, duration):
        self._set_fr(DIRECTIONS["FR"]["BACKWARD"])
        self._set_fl(DIRECTIONS["FL"]["FORWARD"])
        self._set_bl(DIRECTIONS["BL"]["FORWARD"])
        self._set_br(DIRECTIONS["BR"]["BACKWARD"])
        time.sleep(duration)

    def stop(self):
        self._set_fr(DIRECTIONS["FR"]["STOP"])
        self._set_fl(DIRECTIONS["FL"]["STOP"])
        self._set_bl(DIRECTIONS["BL"]["STOP"])
        self._set_br(DIRECTIONS["BR"]["STOP"])

    def put_forks_down(self):
        self._set_forks(FORKS_DOWN)

    def lift_target(self):
        self._set_forks(FORKS_UP)

    def place_target(self):
        self.put_forks_down()
