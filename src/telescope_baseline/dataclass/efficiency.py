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
            'wavelength_grid and efficiency_grid should have the same shape'

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

    def interp(self,wavelength):
        """compute the interpolated value of efficiency

        Args:
            wavelength: wavelength 

        Returns:
            interpolated efficiency

        Examples:
            
            >>> testdata = 'data/teleff.json'
            >>> peclist = pkg_resources.resource_filename('telescope_baseline', testdata)
            >>> efficiency = Efficiency.from_json(speclist)
            >>> wavref=np.linspace(0.8,1.6,1000)
            >>> val=efficiency.interp(wavref)

        """
        val=np.interp(wavelength, self.wavelength_grid, self.efficiency_grid)
        return val

    def weighted_mean(self,wavelength,weight):
        """compute the weighted mean of interpolated efficiency

        Args:
            wavelength: wavelength 
            weight: weight

        Returns:
            weighted mean of efficiency

        Examples:
            
            >>> testdata = 'data/teleff.json'
            >>> peclist = pkg_resources.resource_filename('telescope_baseline', testdata)
            >>> efficiency = Efficiency.from_json(speclist)
            >>> wavref=np.linspace(0.8,1.6,1000)
            >>> weight=np.exp(-(wavref-1.2)**2.0)
            >>> val=efficiency.weighted_mean(wavref,weight)


        """
        assert wavelength.shape == weight.shape, \
            'wavelength and weight should have the same shape'
        return np.sum(self.interp(wavelength)*weight)/np.sum(weight)
        
