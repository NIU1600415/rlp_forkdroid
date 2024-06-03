from abc import ABC, abstractmethod


class Motion(ABC):
    """Abstract base class for robot."""

    @abstractmethod
    def move_forward(self):
        """Move the robot forward."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def move_backward(self):
        """Move the robot backward."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def turn_left(self):
        """Turn the robot left."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def turn_right(self):
        """Turn the robot right."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def stop(self):
        """Stop the robot's movement."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def lift_box(self):
        """Lift the box."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def leave_box(self):
        """Leave the box at the destination."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")
