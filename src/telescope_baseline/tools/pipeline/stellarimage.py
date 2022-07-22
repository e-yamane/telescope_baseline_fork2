import numpy as np
from astropy.nddata import NDData
from photutils import extract_stars, EPSFBuilder
from telescope_baseline.tools.pipeline.simnode import SimNode
from photutils.detection import find_peaks
from astropy.table import Table


class OnDetectorPosition:
    """Hold position on detector, id, and magnitude

    """
    def __init__(self):
        self.__id = 0
        self.__x = 0
        self.__y = 0
        self.__mag = 0


class StellarImage(SimNode):
    """Hold position list in detector coordinate.

    """
    def __init__(self, wcs):
        """Constructor

        Args:
            wcs: world coordinate system of FOV center.

        TODO:
            * maximum pixel number is fixed to 4000 in this implementation. It will be flexible.

        """
        super().__init__()
        self.__wcs = wcs
        self.__parent_list = []
        self.__position_list = []
        self.__pix_max = 4000
        self.__e_psf_stars = None
        self.__e_psf_model = None
        self.__window_size = 9  # window size

    def accept(self, v):
        v.visit(self)

    def get_parent_list(self):
        """ Get parent list.

        Parent object is OnTheSkyCoordinates object. From the position list written in the sky coordinate, calculate
         position list in detector coordinate, and hold it.

        Returns:

        """
        self.__parent_list = self._parent.get_list()

    def world_to_pixel(self):
        """Calculate position in detector coordinate

        Returns: None

        TODO:
            * This class support only galactic coordinate in wcs. It should be more flexible.
            * This implementation not support the gap between detectors.
            * In __position_list x[i][2], number of photon should be flexible, is now assumed to be 3000 and const.

        """
        if "GLON" not in self.__wcs.wcs.ctype[0]:
            print("Coordinate system " + self.__wcs.wcs.ctype[0] + " is not supported")
            raise ValueError
        self.__position_list = []
        for i in range(len(self.__parent_list)):
            self.__position_list.append([self.__parent_list[i].coord.galactic.l.deg,
                                         self.__parent_list[i].coord.galactic.b.deg, 3000])
        self.__position_list = self.__wcs.wcs_world2pix(self.__position_list, 0)
        for i in range(len(self.__position_list)):
            if self.__position_list[i][0] < 0 or self.__position_list[i][1] < 0 \
                    or self.__position_list[i][0] > self.__pix_max or self.__position_list[i][1] > self.__pix_max:
                self.__position_list = np.delete(self.__position_list, i, 0)
        #  for revert conversion use self.__wcs.wcs.wcs_pix2world(pix_array, 0)

    def add_position(self, pos_list):
        """ List of stellar positions

        Args:
            pos_list: ndarray of array (x, y, Nph) where x and y is the position in the pixel coordinate, and Nph is
             number of photons.

        Returns:

        """
        self.__position_list = pos_list

    def get_list(self):
        """ Get observable stellar positions in detector coordinate

        Returns: position list.

        """
        return self.__position_list

    def extract(self):
        """ extract stellar image from the fits data.

        Returns:

        """
        _data = self._child[0].get_hdu().data
        peaks_tbl = find_peaks(_data, threshold=200.)
        half_size = (self.__window_size - 1) / 2
        x = peaks_tbl['x_peak']
        y = peaks_tbl['y_peak']
        mask = ((x > half_size) & (x < (_data.shape[1] - 1 - half_size)) & (y > half_size) &
                (y < (_data.shape[0] - 1 - half_size)))
        stars_tbl = Table()
        stars_tbl['x'] = x[mask]
        stars_tbl['y'] = y[mask]
        nddata = NDData(data=_data)
        self.__e_psf_stars = extract_stars(nddata, stars_tbl, size=self.__window_size)

    def to_photon_num(self):
        """ convert to number of photons

        Returns:
    TODO: Should implement
        """
        pass

    def construct_e_psf(self):
        """ construct effective psf model and fit center with the model

        Returns:

        """
        e_psf_builder = EPSFBuilder(oversampling=4, maxiters=3, progress_bar=True)
        es = self.__e_psf_stars
        self.__e_psf_model, self.__e_psf_stars = e_psf_builder(es)

    def x_match(self):
        """ cross match and add id

        Returns:
    TODO: should implement.
        """
        pass
