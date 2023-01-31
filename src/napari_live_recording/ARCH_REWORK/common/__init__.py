from enum import IntEnum, auto
from dataclasses import dataclass

class WidgetEnum(IntEnum):
    ComboBox = 0
    SpinBox = auto()
    DoubleSpinBox = auto()
    LabeledSlider = auto()
    LineEdit = auto()

class FileFormat(IntEnum):
    TIFF = 0
    # todo: add support for HDF5 storage
    # in the recording
    # HDF5 = auto()

@dataclass
class ROI:
    """Dataclass for ROI settings.
    """
    offset_x: int = 0
    offset_y: int = 0
    height: int = 0
    width: int = 0
    ofs_x_step: int = 1
    ofs_y_step: int = 1
    width_step: int = 1
    height_step: int = 1

    def getPixelSizes(self) -> tuple:
        """Returns the number of pixels along width and height of the current ROI.

        Returns:
            tuple: (height, width) of the ROI.
        """
        return (self.height - self.offset_y, self.width - self.offset_x)