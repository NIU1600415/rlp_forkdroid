from lib.motion import Motion
import time


class SimMotion(Motion):
    """Motion for the simulated robot."""

    def __init__(self, sim):
        """Requires a reference to the client.simulator for CoppeliaSim"""
        self.sim = sim
        self.target_position = None
        self.robot_handle = self.sim.getObject("/RobotnikSummitXL")
        self.bl_handle = self.sim.getObject("/RobotnikSummitXL/back_left_wheel")
        self.br_handle = self.sim.getObject("/RobotnikSummitXL/back_right_wheel")
        self.fl_handle = self.sim.getObject("/RobotnikSummitXL/front_left_wheel")
        self.fr_handle = self.sim.getObject("/RobotnikSummitXL/front_right_wheel")
        self.max_velocity = 3.0  # Can be modified

    def move_forward(self, duration):
        """The right wheel joint directions was set on the other way"""
        self.sim.setJointTargetVelocity(self.bl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, -self.max_velocity)
        if duration:
            time.sleep(duration)
            self.stop()

    def move_backward(self, duration):
        self.sim.setJointTargetVelocity(self.bl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, self.max_velocity)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, duration):
        self.sim.setJointTargetVelocity(self.bl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, -self.max_velocity)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, duration):
        self.sim.setJointTargetVelocity(self.bl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, self.max_velocity)
        if duration:
            time.sleep(duration)
            self.stop()

    def stop(self):
        self.sim.setJointTargetVelocity(self.bl_handle, 0)
        self.sim.setJointTargetVelocity(self.fl_handle, 0)
        self.sim.setJointTargetVelocity(self.br_handle, 0)
        self.sim.setJointTargetVelocity(self.fr_handle, 0)

    def lift_target(self):
        print("LIFT TARGET")

    def place_target(self):
        print("PLACE TARGET")
