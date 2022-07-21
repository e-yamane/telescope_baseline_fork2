from telescope_baseline.tools.pipeline.simnode import SimNode


class SkyPosition():
    """class of hold instantaneous stellar characteristics.

    """
    def __init__(self, num, coord, mag):
        """Constructor

        Args:
            num: ID
            coord: coordinate
            mag: magnitude
        """
        self.__id = num
        self.__coord = coord
        self.__mag = mag

    @property
    def id(self):
        return self.__id

    @property
    def ra(self):
        return self.__coord.gcrs.ra.deg

    @property
    def dec(self):
        return self.__coord.gcrs.dec.deg

    @property
    def coord(self):
        return self.__coord

    @property
    def mag(self):
        return self.__mag


class OnTheSkyPositions(SimNode):
    """Data class of instantaneous stellar positions at a certain time

    """
    def __init__(self, time=None):
        """Constructor

        Args:
            time: astropy.time.Time object which specify the time of this data set.
        """
        super().__init__()
        self.__time = time
        self.__catalogue = None
        self.__position_list = []

    def get_parent_list(self):
        """getting parent information as list

        Returns:None

        """
        self.__catalogue = self._parent.get_list()
        self.__position_list = [None for _ in range(len(self.__catalogue))]

    def add_entry(self, obj: SkyPosition):
        """Add instantaneous position data.

        Args:
            obj: SkyPosition object

        Returns:None

        """
        self.__position_list.append(obj)

    def set_on_the_sky_list(self):
        """Calculate sky coordinate from astrometric parameters

        Returns: None

        """
        for i in range(len(self.__catalogue)):
            c = self.__catalogue[i]
            c1 = c.coord.apply_space_motion(new_obstime=self.__time)
            self.__position_list[i] = SkyPosition(c.id, c1, c.mag)

    def get_time(self):
        """ get time

        Returns:time which is held in this class instance.

        """
        return self.__time

    def get_list(self):
        """

        Returns: list of instantaneous stellar position list.

        """
        return self.__position_list

    def get(self, i):
        """

        Args:
            i: ID

        Returns: instantaneous stellar position object wish ID = i.

        """
        return self.__position_list[i]

    def accept(self, v):
        v.visit(self)
