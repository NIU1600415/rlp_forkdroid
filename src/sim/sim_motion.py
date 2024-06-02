from lib.motion import Motion

class SimMotion(Motion):
    def __init__(self, sim):
        self.sim = sim
        self.target_position = None
        self.robot_handle = self.sim.getObject('/RobotnikSummitXL')
        self.bl_handle = self.sim.getObject('/RobotnikSummitXL/back_left_wheel')
        self.br_handle = self.sim.getObject('/RobotnikSummitXL/back_right_wheel')
        self.fl_handle = self.sim.getObject('/RobotnikSummitXL/front_left_wheel')
        self.fr_handle = self.sim.getObject('/RobotnikSummitXL/front_right_wheel')
        self.max_velocity = 3.0  # Can be modified

    def set_target_position(self, position):
        self.target_position = position

    def get_current_position(self):
        position = self.sim.getObjectPosition(self.robot_handle)
        return position

    '''I struggeld a bit cuz the right wheel joint is set weird'''
    def move_forward(self):
        self.sim.setJointTargetVelocity(self.bl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, -self.max_velocity)

    def move_backward(self):
        self.sim.setJointTargetVelocity(self.bl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, self.max_velocity)

    def turn_left(self):
        self.sim.setJointTargetVelocity(self.bl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, -self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, -self.max_velocity)

    def turn_right(self):
        self.sim.setJointTargetVelocity(self.bl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fl_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.br_handle, self.max_velocity)
        self.sim.setJointTargetVelocity(self.fr_handle, self.max_velocity)

    def stop(self):
        self.sim.setJointTargetVelocity(self.bl_handle, 0)
        self.sim.setJointTargetVelocity(self.fl_handle, 0)
        self.sim.setJointTargetVelocity(self.br_handle, 0)
        self.sim.setJointTargetVelocity(self.fr_handle, 0)


    def lift_box(self):
        pass

    def leave_box(self):
        pass

    def is_arrived(self):
        # current_position = self.get_current_position()
        # if current_position is None or self.target_position is None:
        #     return False

        # threshold = 0.1 # This should be adjusted
        # return (abs(current_position[0] - self.target_position[0]) < threshold and
        #         abs(current_position[1] - self.target_position[1]) < threshold and
        #         abs(current_position[2] - self.target_position[2]) < threshold)
        return False
