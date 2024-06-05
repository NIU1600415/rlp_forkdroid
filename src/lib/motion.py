from abc import ABC, abstractmethod


class Motion(ABC):
    """Abstract base class for robot."""

    @abstractmethod
    def move_forward(self, duration):
        """Move the robot forward."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def move_backward(self, duration):
        """Move the robot backward."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def turn_left(self, duration):
        """Turn the robot left."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def turn_right(self, duration):
        """Turn the robot right."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def stop(self):
        """Stop the robot's movement."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def lift_target(self):
        """Lift the target."""
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def place_target(self):
        """Place the target."""
        raise NotImplementedError("This method should be overridden by subclasses")
