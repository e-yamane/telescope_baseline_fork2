from src.tools.pipeline.simnode import SimNode


class AstrometricCatalogue(SimNode):
    def accept(self, v):
        v.visit(self)
