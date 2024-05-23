from abc import ABC, abstractmethod


class Vision(ABC):
    """Abstract base class for machine vision"""

    @abstractmethod
    def get_image(self, image):
        """Get image from vision sensor (camera). Returns image data and resolution."""
