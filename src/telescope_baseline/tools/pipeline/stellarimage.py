import numpy as np
from astropy.wcs import WCS
from telescope_baseline.tools.pipeline.simnode import SimNode


class OnDetectorPosition:
    """Hold position on detector, id, and manitude

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
        """Calcolate position in detector coordinate

        Returns: None

        TODO:
            * This class support only galactic coordinate in wcs. It should be more flexible.
            * This implementation not support the gap between detectors.
            * __position_list should contain number of photons in x[i][2]

        """
        if "GLON" not in self.__wcs.wcs.ctype[0]:
            print("Coordinate system " + self.__wcs.wcs.ctype[0] + " is not supported")
            raise ValueError
        self.__position_list = []
        for i in range(len(self.__parent_list)):
            self.__position_list.append([self.__parent_list[i].coord.galactic.l.deg,
                                         self.__parent_list[i].coord.galactic.b.deg])
        self.__position_list = self.__wcs.wcs_world2pix(self.__position_list, 0)
        for i in range(len(self.__position_list)):
            if self.__position_list[i][0] < 0 or self.__position_list[i][1] < 0 \
                    or self.__position_list[i][0] > self.__pix_max  or self.__position_list[i][1] > self.__pix_max:
                self.__position_list = np.delete(self.__position_list, i, 0)
        #  for revert conversion use self.__wcs.wcs.wcs_pix2world(pix_array, 0)

    def add_position(self, list):
        """ List of stellar positions

        Args:
            list: ndarray of array (x, y, Nph) where x and y is the position in the pixel coordinate, and Nph is
             number of photons.

        Returns:

        """
        self.__position_list = list

    def get_list(self):
        """ Get observable stellar positions in detector coordinate

        Returns: position list.

        """
        return self.__position_list
