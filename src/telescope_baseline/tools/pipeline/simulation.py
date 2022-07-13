from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from visitor import SimVisitor


class Simulation(SimVisitor):
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

    def visit_os(self, obj: OnTheSkyPosition):
        # if obj.has_parent():
        #     obj.parent.get_list()
        # set_stellar_position
        print("os")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)

    def visit_ap(self, obj: AstrometricCatalogue):
        # non operation
        print("ap")
        for i in range(obj.get_child_size()):
            obj.get_child(i).accept(self)


if __name__ == '__main__':
    # generate object structure
    a = AstrometricCatalogue()
    o = []
    for i in range(10):
        o.append(OnTheSkyPosition())
    for i in range(len(o)):
        a.add_child(o[i])
    v = Simulation()
    a.accept(v)
    # call accept method for top.
    print("hello")