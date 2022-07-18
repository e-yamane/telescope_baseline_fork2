from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskypositions import OnTheSkyPositions
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from visitor import SimVisitor


class Analysis(SimVisitor):
    def visit_di(self, obj: DetectorImage):
        # non operation
        pass

    def visit_si(self, obj: StellarImage):
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)
        # extract()
        # to_photon_num()
        # construct_epsf()
        # xmatch()

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
    # generate object structure
    a = AstrometricCatalogue()
    o = []
    for i in range(10):
        o.append(OnTheSkyPositions())
    for i in range(len(o)):
        a.add_child(o[i])
    v = Analysis()
    a.accept(v)
    # call accept method for top.
    print("hello")