import dataclasses
import numpy as np
import json


@dataclasses.dataclass(frozen=True)
class Efficiency:
    """This class defines the wavelength dependent efficiency.

    Attributes:
        wavelength (ndarray): Wavelengths in micron.
        efficiency (ndarray): Efficiencies.
        title (str): Title of the data.
        comment (str): Comments.
    """
    # set sample data as default
    wavelength: np.ndarray = np.array([0.9, 1.6])
    efficiency: np.ndarray = np.array([0.85, 0.85])
    title:      str = 'Default'
    comment:    str = 'default value'

    @classmethod
    def __post_init__(self):
        assert self.wavelength.shape == self.efficiency.shape, \
            'wavelength and efficiency should have the same shape'

    def from_json(cls, filename):
        """This method creates efficiency array data depend on wavelength.

        Args:
            filename: Input json filename.

        Returns:
            Efficiency: Created efficiency object.
        """
        with open(filename, 'r') as fp:
            js = json.load(fp)
            wavelength = np.array(js['wavelength'])
            efficiency = np.array(js['efficiency'])
            if 'title' in js:
                title = js['title']
            if 'comment' in js:
                comment = js['comment']

        wlefic = Efficiency(
            wavelength=wavelength,
            efficiency=efficiency,
            title=title,
            comment=comment)

        return wlefic
