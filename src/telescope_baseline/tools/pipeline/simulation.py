from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions, SkyPosition
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
from visitor import SimVisitor
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord
import numpy as np
from astropy import wcs
from astropy.io import fits


class Simulation(SimVisitor):
    """Visitor class for generate pseudo data.

    Pipeline processing is realized by Visitor. Simulation will be done from Astrometric catalogue downward to detector
     image, direction opposite to analysis. This is inherited from SimVisitor class in visitor.py.  This class
     implements visit_di, visit_si, visit_os and visit_ap methods, which is defined abstract methods in the super-class.

    """
    def visit_di(self, obj: DetectorImage):
        # if obj.has_parent():
        #     obj.parent.get_list()
        #  makeimage() # generate fits
        pass

    def visit_si(self, obj: StellarImage):
        print("si")
        if obj.has_parent():
            obj.get_parent_list()
            obj.world_to_pixel()
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)

    def visit_os(self, obj: OnTheSkyPositions):
        print("os")
        if obj.has_parent():
            obj.get_parent_list()
            obj.set_on_the_sky_list()
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)

    def visit_ap(self, obj: AstrometricCatalogue):
        # non operation
        print("ap")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)


if __name__ == '__main__':
    t = Time('2000-01-01 00:00:00.0')
    c1 = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic")
    c2 = SkyCoord(l=0, b=0.1, unit=('deg', 'deg'), frame="galactic")
    c3 = SkyCoord(l=0, b=1.0, unit=('deg', 'deg'), frame="galactic")

    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4,0], [0,1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]

    o = OnTheSkyPositions(t)
    o.add_entry(SkyPosition(1, c1, 12.5))
    o.add_entry(SkyPosition(2, c2, 12.0))
    o.add_entry(SkyPosition(3, c3, 13.5))
    s = StellarImage(w)
    o.add_child(s)

    v = Simulation()
    o.accept(v)

    print(s.get_list())

