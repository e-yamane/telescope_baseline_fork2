from telescope_baseline.tools.pipeline.simnode import SimNode


class OnTheSkyPositions(SimNode):
    def __init__(self, time):
        super().__init__()
        self.__time = time
        self.__catalogue = None
        self.__position_list = []

    def get_parent_list(self):
        self.__catalogue = self._parent.get_list()
        self.__position_list = [None for _ in range(len(self.__catalogue))]

    def set_on_the_sky_list(self):
        for i in range(len(self.__catalogue)):
            c = self.__catalogue[i]
            c1 = c.coord.apply_space_motion(new_obstime=self.__time)
            self.__position_list[i] = SkyPosition(c.id, c1, c.mag)

    def get(self, i):
        return self.__position_list[i]

    def accept(self, v):
        v.visit(self)


class SkyPosition():
    def __init__(self, num, coord, mag):
        self.__id = num
        self.__ra = coord.gcrs.ra.deg
        self.__dec = coord.gcrs.dec.deg
        self.__mag = mag

    @property
    def id(self):
        return self.__id

    @property
    def ra(self):
        return self.__ra

    @property
    def dec(self):
        return self.__dec

    @property
    def mag(self):
        return self.__mag

