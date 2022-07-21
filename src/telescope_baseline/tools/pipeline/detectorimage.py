import numpy as np
from astropy.io import fits

from telescope_baseline.tools.pipeline.simcomponent import SimComponent


class DetectorImage(SimComponent):
    """Data hold class for detector whole image.

    Attributes:
        __parent_list: parent position list with number of photons
        __nx: number of pixel in x direction
        __ny: number of pixel in u direction
        __psf_w: psf width in pixel unit.
        __array: ndarray of pixel data
        __hdu: fits primary hdu

    Todo:
        * detector format should be flexible
        * PSF shape should be flexible, is now assumed as Gaussian

    """
    def __init__(self):
        super().__init__()
        self.__parent_list = []
        self.__nx = 100
        self.__ny = 100
        self.__psf_w = 1.0
        self.__array = []
        self.__hdu = fits.PrimaryHDU()

    def get_child_size(self):
        pass

    def get_child(self, i: int):
        pass

    def get_parent_list(self):
        """ Get parent list.

        Parent object is OnTheSkyCoordinates object. From the position list written in the sky coordinate, calculate
         position list in detector coordinate, and hold it.

        Returns:

        """
        self.__parent_list = self._parent.get_list()

    def make_image(self):
        self.__array = np.random.uniform(0.0, 10.0, (self.__nx, self.__ny))
        for s in self.__parent_list:
            for j in range(int(s[2])):
                xp = int(self.__psf_w * np.random.randn() + s[1] + 0.5)
                yp = int(self.__psf_w * np.random.randn() + s[0] + 0.5)
                if 0 <= xp < self.__nx and 0 <= yp < self.__ny:
                    self.__array[xp][yp] += 1

    def make_fits(self):
        self.__hdu = fits.PrimaryHDU()
        self.__hdu.data = self.__array
        return self.__hdu

    def accept(self, v):
        v.visit(self)
