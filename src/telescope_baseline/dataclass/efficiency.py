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
    wavelength_grid: np.ndarray = np.array([0.9, 1.6])
    efficiency_grid: np.ndarray = np.array([0.85, 0.85])
    title:      str = 'Default'
    comment:    str = 'default value'

    def __post_init__(self):
        assert self.wavelength_grid.shape == self.efficiency_grid.shape, \
            'wavelength and efficiency should have the same shape'

    @classmethod
    def from_json(cls, filename):
        """This method creates efficiency array data depend on wavelength.

        Args:
            filename: Input json filename.

        Returns:
            Efficiency: Created efficiency object.
        """
        with open(filename, 'r') as fp:
            js = json.load(fp)
            wavelength_grid = np.array(js['wavelength'])
            efficiency_grid = np.array(js['efficiency'])
            if 'title' in js:
                title = js['title']
            if 'comment' in js:
                comment = js['comment']

        wlefic = Efficiency(
            wavelength_grid=wavelength_grid,
            efficiency_grid=efficiency_grid,
            title=title,
            comment=comment)

        return wlefic

    def efficiency_interp(self,wavelength):
        """compute the interpolated value of efficiency

        Args:
            wavelength: wavelength 

        Returns:
            interpolated efficiency
        """
        val=np.interp(wavelength, self.wavelength_grid, self.efficiency_grid)
        return val
