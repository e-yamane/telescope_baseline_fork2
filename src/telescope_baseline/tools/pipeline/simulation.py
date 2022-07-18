from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from telescope_baseline.tools.pipeline.catalogue_entry import CatalogueEntry
from visitor import SimVisitor
import astropy.units as u
import astropy.coordinates
from astropy.time import Time
from astropy.coordinates import SkyCoord


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
        # if obj.has_parent():
        #     obj.parent.get_list()
        # world_to_pixel()
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)

    def visit_os(self, obj: OnTheSkyPositions):
        # if obj.has_parent():
        #     obj.parent.get_list()
        # set_stellar_position
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
    t = [Time('2000-01-01 00:00:00.0'), Time('2000-02-01 00:00:00.0'), Time('2000-03-01 00:00:00.0'),
         Time('2000-04-01 00:00:00.0'), Time('2000-05-01 00:00:00.0'), Time('2000-06-01 00:00:00.0'),
         Time('2000-07-01 00:00:00.0'), Time('2000-08-01 00:00:00.0'), Time('2000-09-01 00:00:00.0'),
         Time('2000-10-01 00:00:00.0'), Time('2000-11-01 00:00:00.0'), Time('2000-12-01 00:00:00.0'),
         Time('2001-01-01 00:00:00.0')]
    c1 = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=100 * u.pc, obstime=t[0],
                  pm_l_cosb=0 * u.mas / u.yr, pm_b=0 * u.mas / u.yr)
    c2 = SkyCoord(l=0, b=0, unit=('deg', 'deg'), frame="galactic", distance=1 * u.pc, obstime=t[0],
                  pm_l_cosb=-1000 * u.mas / u.yr, pm_b=1200 * u.mas / u.yr)
    a = AstrometricCatalogue()
    a.add_entry(CatalogueEntry(1, c1, 12.5))
    a.add_entry(CatalogueEntry(2, c2, 12.5))

    o = []
    for i in range(len(t)):
        o.append(OnTheSkyPositions(t[i]))
    for i in range(len(o)):
        a.add_child(o[i])
    v = Simulation()
    a.accept(v)

    # call accept method for top.
    print("---")
    for i in range(len(o)):
        c = o[i].get(0)
        print(str(c.ra) + "," + str(c.dec))
    print("---")
    for i in range(len(o)):
        sc1 = c1.apply_space_motion(new_obstime=t[i])
        print(str(sc1.gcrs.ra.deg) + "," + str(sc1.gcrs.dec.deg))
    print(c2.icrs.ra.deg)
    print(c2.icrs.dec.deg)