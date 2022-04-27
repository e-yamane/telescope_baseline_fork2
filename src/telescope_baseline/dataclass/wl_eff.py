import dataclasses
import numpy as np
import json

@dataclasses.dataclass(frozen=True)
class WlEfic:
    """
    This class defines the wavelength dependent efficiency

    Attributes:
        wavelength (ndarray): Wavelengths in micron.
        efficiency (ndarray): Efficiencies.
        title (str): Title of the data
        comment (str): Comments
    """
    wavelength: np.ndarray = np.array([0.9,1.6])
    efficiency: np.ndarray = np.array([0.85, 0.85]) # sample data
    title:      str = 'Default'
    comment:    str = 'default value'

    @classmethod
    def from_json(cls, filename):
        """
        This method creates efficiency array data depend on wavelength

        Args:
            filename: Input json filename.

        Returns:
            WlEfic: Created efficiency object.
        """
        with open(filename, "r") as fp:
            js = json.load(fp)
            wavelength = np.array(js['wavelength'])
            efficiency = np.array(js['efficiency'])
            if 'title' in js:
                title = js['title']
            if 'comment' in js:
                comment = js['comment']

        wlefic = WlEfic(
            wavelength = wavelength,
            efficiency = efficiency,
            title      = title,
            comment    = comment)

        return wlefic
