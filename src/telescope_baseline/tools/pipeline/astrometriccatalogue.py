from telescope_baseline.tools.pipeline.simnode import SimNode
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
import astropy.units as u


class AstrometricCatalogue(SimNode):
    def __init__(self):
        super().__init__()
        self.__catalogue = []

    def accept(self, v):
        v.visit(self)

    def add_entry(self, c:CatalogueEntry):
        self.__catalogue.append(c)

    def get_list(self):
        return self.__catalogue

    def save(self, filename):
        f = open(filename, 'w')
        for i in range(len(self.__catalogue)):
            f.write(str(self.__catalogue[i].id) +"," + str(self.__catalogue[i].ra) + "," +
                    str(self.__catalogue[i].dec) + "," + str(self.__catalogue[i].parallax / u.mas) + "," +
                    str(self.__catalogue[i].pm_ra * u.yr / u.mas) + "," +
                    str(self.__catalogue[i].pm_dec * u.yr / u.mas) + "\n")
