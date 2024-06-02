from lib.motion import Motion


class SimMotion(Motion):
    """Motion for the simulated robot."""

    def __init__(self, sim):
        """Requires a reference to the client.simulator for CoppeliaSim"""
        self.sim = sim

    def move_forward(self):
        pass

    def move_backward(self):
        pass

    def turn_left(self):
        pass

    def turn_right(self):
        pass

    def stop(self):
        pass
