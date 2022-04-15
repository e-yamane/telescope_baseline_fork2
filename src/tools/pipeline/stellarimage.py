from src.tools.pipeline.simnode import SimNode


class StellarImage(SimNode):
    def accept(self, v):
        v.visit(self)