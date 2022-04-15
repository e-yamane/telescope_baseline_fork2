from src.tools.pipeline.astrometriccatalogue import AstrometricCatalogue
from src.tools.pipeline.detectorimage import DetectorImage
from src.tools.pipeline.ontheskyposition import OnTheSkyPosition
from src.tools.pipeline.stellarimage import StellarImage
from visitor import SimVisitor


class Analysis(SimVisitor):
    def visit_di(self, obj: DetectorImage):
        pass

    def visit_si(self, obj: StellarImage):
        pass

    def visit_os(self, obj: OnTheSkyPosition):
        pass

    def visit_ap(self, obj: AstrometricCatalogue):
        pass
