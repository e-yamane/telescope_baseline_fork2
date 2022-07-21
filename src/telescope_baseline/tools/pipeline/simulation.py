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

    TODO: output fits file name should be flexible.
    TODO: in visit_di, if output list is empty, raise exception.

    """
    def visit_di(self, obj: DetectorImage):
        print("di")
        if obj.has_parent():
            obj.get_parent_list()
        # raise exception if the list is empty
        obj.make_image()  # generate fits
        a = obj.make_fits()
        a.writeto("output.fits", overwrite=True)

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
    pos = np.array([[50, 50, 1000],[28, 80, 1000]], dtype=np.float64)
    w = wcs.WCS(naxis=2)
    w.wcs.crpix = [256, 256]  # Reference point in pixel
    w.wcs.cd = [[1.31e-4,0], [0,1.31e-4]]  # cd matrix
    w.wcs.crval = [0, 0]  #
    w.wcs.ctype = ["GLON-TAN", "GLAT-TAN"]

    s = StellarImage(w)
    s.add_position(pos)
    d = DetectorImage()
    s.add_child(d)

    v = Simulation()
    s.accept(v)

    print(s.get_list())

