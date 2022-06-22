from telescope_baseline.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from telescope_baseline.tools.pipeline.detectorimage import DetectorImage
from telescope_baseline.tools.pipeline.ontheskyposition import OnTheSkyPosition
from telescope_baseline.tools.pipeline.stellarimage import StellarImage
from visitor import SimVisitor


class Simulation(SimVisitor):
    def visit_di(self, obj: DetectorImage):
        pass

    def visit_si(self, obj: StellarImage):
        pass

    def visit_os(self, obj: OnTheSkyPosition):
        pass

    def visit_ap(self, obj: AstrometricCatalogue):
        pass