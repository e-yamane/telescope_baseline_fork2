from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from visitor import SimVisitor
from astropy import wcs


class Analysis(SimVisitor):
    def visit_di(self, obj: DetectorImage):
        try:
            obj.load("output.fits")
        except FileNotFoundError:
            print('file not found.')

    def visit_si(self, obj: StellarImage):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        obj.extract()
        obj.to_photon_num()
        obj.construct_e_psf()
        obj.x_match()

    def visit_os(self, obj: OnTheSkyPositions):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        print("os")
        # solve_distortion()
        # map_to_the_sky()

    def visit_ap(self, obj: AstrometricCatalogue):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        print("ap")
        # calculate_ap_parameters()


if __name__ == '__main__':
    w = wcs.WCS(naxis=2)
    w.crpix = [256, 256]  # Reference point in pixel
    w.cd = [[1.31e-4, 0], [0, 1.31e-4]]  # cd matrix
    w.crval = [0, 0]  #
    w.ctype = ["GLON-TAN", "GLAT-TAN"]
    d = DetectorImage()
    s = StellarImage(w)
    s.add_child(d)

    v = Analysis()
    s.accept(v)
