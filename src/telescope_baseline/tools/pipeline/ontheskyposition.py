from telescope_baseline.tools.pipeline.simnode import SimNode


class OnTheSkyPosition(SimNode):
    def accept(self, v):
        v.visit(self)
