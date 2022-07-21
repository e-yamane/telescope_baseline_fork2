from telescope_baseline.tools.pipeline.simnode import SimNode
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
import astropy.units as u


class AstrometricCatalogue(SimNode):
    """AstrometricCatalogue class is the correction class of CatalogueEntry.

    The constructor is default constructor. After instantiate the class, entry is added by add_entry(c) method. The
     variable c is the CatalogueEntry object.

    """
    def __init__(self):
        super().__init__()
        self.__catalogue = []

    def accept(self, v):
        v.visit(self)

    def add_entry(self, c:CatalogueEntry):
        """add catalogue entry to the AstrometricCatalogue object.

        Args:
            c: CatalogueEntry object

        Returns:Non

        """
        self.__catalogue.append(c)

    def get_list(self):
        """

        Returns:The array of CatalogueEntry object.

        """
        return self.__catalogue

    def save(self, filename):
        """The method for save the catalogue to the file.

        Args:
            filename: The name of the file for saving data.

        Returns: Non

        """
        f = open(filename, 'w')
        for i in range(len(self.__catalogue)):
            f.write(str(self.__catalogue[i].id) +"," + str(self.__catalogue[i].ra) + "," +
                    str(self.__catalogue[i].dec) + "," + str(self.__catalogue[i].parallax / u.mas) + "," +
                    str(self.__catalogue[i].pm_ra * u.yr / u.mas) + "," +
                    str(self.__catalogue[i].pm_dec * u.yr / u.mas) + "\n")
