from abc import ABC, abstractmethod
import numpy.typing as npt
from numpy import uint8


class Vision(ABC):
    """Abstract base class for machine vision"""

    @abstractmethod
    def get_frame(self) -> npt.NDArray[uint8]:
        """Get an RGB image frame from vision sensor (camera). Returns numpy image data."""
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def detect_box(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    @abstractmethod
    def detect_dest(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses")

    def is_arrived(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses")
